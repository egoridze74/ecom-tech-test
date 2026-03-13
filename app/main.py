from fastapi import FastAPI, UploadFile, File, HTTPException

import app.crud as crud
import app.upload as upload
from app.schemas import UploadResponse, StudentTwos


app = FastAPI()


@app.post("/upload-grades", response_model=UploadResponse)
async def upload_grades(file: UploadFile = File(...)):
    try:
        records = await upload.parse_csv_file(file)
        records_loaded, students_count = await crud.insert_grades(records)
        return UploadResponse(
            status="ok", records_loaded=records_loaded, students=students_count
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Ошибка сервера: {str(e)}")


@app.get("/students/more-than-3-twos", response_model=list[StudentTwos])
async def students_more_than_3_twos():
    try:
        students = await crud.get_students_more_than_3_twos()
        return [dict(row) for row in students]
    except Exception as e:
        raise HTTPException(500, f"Ошибка сервера: {str(e)}")


@app.get("/students/less-than-5-twos", response_model=list[StudentTwos])
async def students_less_than_5_twos():
    try:
        students = await crud.get_students_less_than_5_twos()
        return [dict(row) for row in students]
    except Exception as e:
        raise HTTPException(500, f"Ошибка сервера: {str(e)}")


@app.get("/")
async def root():
    return {
        "message": "API готов к работе. Доступные ручки: '/upload-grades', '/students/more-than-3-twos', '/students/less-than-5-twos'"
    }
