from mod.logs import Logger
from mod.sql import SqlTable, SqlColumns
from mod.dao import MyConn, SqlStatement
from mod.preprocess import pt, op, dx, dates


# EDI.xlsx
EDI_TABLE = SqlTable("edi_dl", "hecon")
EDI_COLUMN = {
    "code": "varchar(200)",  # 물품코드
    "name": "varchar(200)",  # 물품명
    "standard": "varchar(200)",  # 규격
    "is_insured": "varchar(200)",  # 보험구분
    "unit": "varchar(200)",  # 단위 EA, or BOX
    "trade": "varchar(200)",  # 거래처
    "account": "varchar(200)",  # 입고계정
    "edi": "varchar(200)",  # EDI
    "edisub": "varchar(200)",  # (자)EDI코드
}

# 물류_DX.csv
DX_TABLE = SqlTable("dx_dl", "hecon")
DX_COLUMN = {
    "id": "varchar(200)",
    "date": "varchar(200)",
    "value": "int",
}

# 물류_OP.csv
OP_TABLE = SqlTable("op_dl", "hecon")
OP_COLUMN = {
    "id": "varchar(200)",
    "date": "varchar(200)",
    "value": "int",
}

# 물류_PT.csv
PT_TABLE = SqlTable("pt_dl", "hecon")
PT_COLUMN = {
    "id": "varchar(200)",
    "date": "varchar(200)",
    "value": "int",
}

DATE_TABLE = SqlTable("dt", "hecon")
DATE_COLUMN = {
    "date": "varchar(200)",
    "year": "varchar(5)",
    "month": "varchar(5)",
    "day": "varchar(5)",
    "weekday": "int",
}


if __name__ == "__main__":
    # Database access object
    l = Logger()
    conn = MyConn("127.0.0.1", "hecon", l, True)

    try:
        # Check connection to the database
        conn.ping()
    except BaseException:
        raise RuntimeError("failed to connect to database")

    # Create table
    builder = SqlStatement()

    # data lakes
    conn.wrap(builder.create_table, table=EDI_TABLE, table_columns=SqlColumns(EDI_COLUMN).typewise)
    conn.wrap(builder.create_index, table=EDI_TABLE, table_columns=["code"])

    conn.wrap(builder.create_table, table=DX_TABLE, table_columns=SqlColumns(DX_COLUMN).typewise)
    conn.wrap(builder.create_index, table=DX_TABLE, table_columns=["id", "date"])

    conn.wrap(builder.create_table, table=OP_TABLE, table_columns=SqlColumns(OP_COLUMN).typewise)
    conn.wrap(builder.create_index, table=OP_TABLE, table_columns=["id", "date"])

    conn.wrap(builder.create_table, table=PT_TABLE, table_columns=SqlColumns(PT_COLUMN).typewise)
    conn.wrap(builder.create_index, table=PT_TABLE, table_columns=["id", "date"])

    # Insert data - do not have to be processed. Raw data
    # Patiens
    pt_col, pt_clean = pt()
    conn.wrapmany(builder.create_data, table=PT_TABLE, table_columns=pt_col, data=pt_clean)

    # Operation
    op_col, op_clean = op()
    conn.wrapmany(builder.create_data, table=OP_TABLE, table_columns=op_col, data=op_clean)

    # Diagnosis
    dx_col, dx_clean = dx()
    conn.wrapmany(builder.create_data, table=DX_TABLE, table_columns=dx_col, data=dx_clean)

    # Create `Date` table
    conn.wrap(builder.create_table, table=DATE_TABLE, table_columns=SqlColumns(DATE_COLUMN).typewise)
    conn.wrap(builder.create_index, table=DATE_TABLE, table_columns=["date"])

    date_col, date_clean = dates()
    conn.wrapmany(builder.create_data, table=DATE_TABLE, table_columns=date_col, data=date_clean)

    # Create table entity join
    fk_dx_date = """
        ALTER TABLE dx_dl
        ADD CONSTRAINT fk_dx_dl_date
        FOREIGN KEY (date) REFERENCES dt(date);
    """
    fk_op_date = """
        ALTER TABLE op_dl
        ADD CONSTRAINT fk_op_dl_date
        FOREIGN KEY (date) REFERENCES dt(date);
    """
    fk_pt_date = """
        ALTER TABLE pt_dl
        ADD CONSTRAINT fk_pt_dl_date
        FOREIGN KEY (date) REFERENCES dt(date);
    """
    conn.wrap(builder.send_raw, script=fk_dx_date)
    conn.wrap(builder.send_raw, script=fk_op_date)
    conn.wrap(builder.send_raw, script=fk_pt_date)

    # Delete test
    # conn.wrap(builder.delete_table, table=PT_TABLE)
    # conn.wrap(builder.delete_table, table=DX_TABLE)
    # conn.wrap(builder.delete_table, table=OP_TABLE)
