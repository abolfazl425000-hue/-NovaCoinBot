import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client


app = FastAPI(title="NovaCoin API")


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase environment variables are missing")


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


class TapRequest(BaseModel):
    telegram_id: int


@app.get("/")
def home():
    return {
        "status": "ok",
        "service": "NovaCoin API"
    }


@app.get("/user/{telegram_id}")
def get_user(telegram_id: int):

    result = (
        supabase
        .table("users")
        .select("telegram_id,username,first_name,balance,energy,max_energy")
        .eq("telegram_id", telegram_id)
        .limit(1)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return result.data[0]


@app.post("/tap")
def tap(request: TapRequest):

    result = (
        supabase
        .table("users")
        .select("telegram_id,balance,energy,max_energy")
        .eq("telegram_id", request.telegram_id)
        .limit(1)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user = result.data[0]

    energy = user["energy"] or 0
    balance = user["balance"] or 0

    if energy <= 0:
        raise HTTPException(
            status_code=400,
            detail="Not enough energy"
        )

    new_balance = balance + 1
    new_energy = energy - 1

    updated = (
        supabase
        .table("users")
        .update({
            "balance": new_balance,
            "energy": new_energy
        })
        .eq("telegram_id", request.telegram_id)
        .execute()
    )

    if not updated.data:
        raise HTTPException(
            status_code=500,
            detail="Database update failed"
        )

    return {
        "success": True,
        "balance": new_balance,
        "energy": new_energy
    }
