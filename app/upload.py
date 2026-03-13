import pandas as pd
from io import BytesIO
from fastapi import UploadFile, HTTPException

from app.schemas import GradeRecord


async def parse_csv_file(file: UploadFile) -> list[GradeRecord]:
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            400, "Неверный формат файла. Обрабатываются только csv файлы"
        )

    content = await file.read()

    try:
        df = pd.read_csv(BytesIO(content), sep=";", dtype={"Оценка": "int8"})
    except Exception as e:
        raise HTTPException(400, f"Ошибка чтения файла: {str(e)}")

    required_cols = ["Дата", "Номер группы", "ФИО", "Оценка"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise HTTPException(400, f"Отсутствуют колонки: {missing}")

    records = []
    for idx, row in df.iterrows():
        try:
            records.append(
                GradeRecord(
                    date=pd.to_datetime(row["Дата"], format="%d.%m.%Y").date(),
                    group_name=str(row["Номер группы"]),
                    student_name=str(row["ФИО"]),
                    grade=int(row["Оценка"]),
                )
            )
        except Exception as e:
            raise HTTPException(400, f"Ошибка в строке {idx + 1}: {str(e)}")

    return records
