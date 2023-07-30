from mod.logs import Logger
from mod.dao import MyConn, SqlStatement

from data_lake import PT_TABLE, OP_TABLE, DX_TABLE


def main():
    l = Logger()
    conn = MyConn("127.0.0.1", "hecon", l, True)
    builder = SqlStatement()

    pt = conn.wrap(builder.read_data, table=PT_TABLE)
    op = conn.wrap(builder.read_data, table=OP_TABLE)
    dx = conn.wrap(builder.read_data, table=DX_TABLE)

    return pt, op, dx


if __name__ == "__main__":
    data = main()
    