from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import boto3
from datetime import datetime
import uuid
from dotenv import load_dotenv
import os
from decimal import Decimal

load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 로컬 개발용
        "http://127.0.0.1:3000",  # 로컬 개발용
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# AWS 클라이언트 설정
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
bucket_name = os.getenv('S3_BUCKET_NAME')
table_name = os.getenv('DYNAMODB_TABLE_NAME')

# AWS 서비스 클라이언트 초기화
s3 = boto3.client('s3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

comprehend = boto3.client('comprehend',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

# DynamoDB 테이블
table = dynamodb.Table(table_name)

# 요약 모델 초기화
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

class TextInput(BaseModel):
    text: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # S3에 파일 업로드
        file_key = f"inputs/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        s3.upload_fileobj(file.file, bucket_name, file_key)
        
        # S3에서 파일 읽기
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        text_content = response['Body'].read().decode('utf-8')
        
        return {"filename": file.filename, "text_content": text_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize_text(input_data: TextInput):
    try:
        print("Received text:", input_data.text)  # 입력 텍스트 로깅
        
        # 텍스트 요약
        summary = summarizer(input_data.text, max_length=130, min_length=30, do_sample=False)
        print("Summary generated:", summary)  # 요약 결과 로깅
        
        # AWS Comprehend 감정 분석
        sentiment = comprehend.detect_sentiment(
            Text=input_data.text,
            LanguageCode='en'
        )
        print("Sentiment analysis:", sentiment)  # 감정 분석 결과 로깅
        
        # float를 Decimal로 변환
        sentiment_scores = {
            k: Decimal(str(v)) 
            for k, v in sentiment['SentimentScore'].items()
        }
        
        # DynamoDB에 저장
        item = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'original_text': input_data.text,
            'summary': summary[0]['summary_text'],
            'sentiment': sentiment['Sentiment'],
            'sentiment_scores': sentiment_scores
        }
        
        table.put_item(Item=item)
        
        return {
            "summary": summary[0]['summary_text'],
            "sentiment": sentiment['Sentiment']
        }
    except Exception as e:
        print("Error occurred:", str(e))  # 에러 로깅
        import traceback
        print("Traceback:", traceback.format_exc())  # 상세 에러 추적
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)