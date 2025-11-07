import pandas as pd
import pytest
from _supporting.schemas.pos import POS, coerce_utc
from _supporting.schemas.weather import Weather
from _supporting.schemas.ref import SKURef

def test_pos_schema_header_only():
    df = pd.DataFrame(columns=["store_id","sku_id","ts","qty","price","promo_flag","stock_out_flag"])
    df = coerce_utc(df, "ts")
    POS.validate(df)

def test_weather_schema_header_only():
    df = pd.DataFrame(columns=["store_id","ts","temp_c","precip_mm","is_holiday","event_id"])
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    Weather.validate(df)

def test_ref_schema_header_only():
    df = pd.DataFrame(columns=["store_id","sku_id","category","brand","size","cost"])
    SKURef.validate(df)
