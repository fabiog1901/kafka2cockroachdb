
SET CLUSTER SETTING cluster.organization = 'Workshop';
SET CLUSTER SETTING enterprise.license = 'crl-0-xxxxxxxxxxxxx';

SET CLUSTER SETTING kv.snapshot_rebalance.max_rate = '256MiB';
SET CLUSTER SETTING kv.snapshot_recovery.max_rate = '256MiB';

-- avoid complications with scram-sha-256 by using old encryption mechanism
SET CLUSTER SETTING server.user_login.password_encryption = 'crdb-bcrypt';

CREATE USER IF NOT EXISTS cockroach WITH password 'cockroach';
GRANT admin TO cockroach;

USE defaultdb;

CREATE TABLE IF NOT EXISTS orders (
    acc_loc STRING NOT NULL,
    acc_num STRING NOT NULL,
    ts TIMESTAMPTZ NOT NULL,
    c_ts INT8 NOT NULL,
    send_timestamp TIMESTAMPTZ,
    user_id STRING,
    quantity INT8,
    side STRING,
    price DECIMAL,
    is_contra BOOL,
    symbol STRING,
    created_time TIMESTAMPTZ DEFAULT now(),
    col001 STRING,
    col002 STRING,
    col003 STRING,
    col004 STRING,
    col005 STRING,
    col006 STRING,
    col007 STRING,
    col008 STRING,
    col009 STRING,
    col010 STRING,
    col011 STRING,
    col012 STRING,
    col013 STRING,
    col014 STRING,
    col015 STRING,
    col016 STRING,
    col017 STRING,
    col018 STRING,
    col019 STRING,
    col020 STRING,
    col030 STRING,
    col031 STRING,
    col032 STRING,
    col033 STRING,
    col034 STRING,
    col035 STRING,
    col036 STRING,
    col037 STRING,
    col038 STRING,
    col039 STRING,
    col040 STRING,
    col101 INT8,
    col102 INT8,
    col103 INT8,
    col104 INT8,
    col105 INT8,
    col106 INT8,
    col107 INT8,
    col108 INT8,
    col109 INT8,
    col110 INT8,
    col111 INT8,
    col112 INT8,
    col113 INT8,
    col114 INT8,
    col115 INT8,
    col116 INT8,
    col117 INT8,
    col118 INT8,
    col119 INT8,
    col120 INT8,
    col201 BOOL,
    col202 BOOL,
    col203 BOOL,
    col204 BOOL,
    col205 BOOL,
    col206 BOOL,
    col207 BOOL,
    col208 BOOL,
    col209 BOOL,
    col210 BOOL,
    col211 BOOL,
    col212 BOOL,
    col213 BOOL,
    col214 BOOL,
    col215 BOOL,
    col216 BOOL,
    col217 BOOL,
    col218 BOOL,
    col219 BOOL,
    col220 BOOL,
    CONSTRAINT orders_pkey PRIMARY KEY (acc_loc ASC, acc_num ASC, ts ASC, c_ts ASC)
);

-- using a service account that can only View Storage
IMPORT INTO orders (
    acc_loc, acc_num, ts, c_ts,
    send_timestamp, user_id, quantity, side,
    price, is_contra, symbol, created_time,
    col001, col002, col003, col004, col005, col006, col007, col008, col009, col010,
    col011, col012, col013, col014, col015, col016, col017, col018, col019, col020,
    col030, col031, col032, col033, col034, col035, col036, col037, col038, col039,
    col040, col101, col102, col103, col104, col105, col106, col107, col108, col109,
    col110, col111, col112, col113, col114, col115, col116, col117, col118, col119,
    col120, col201, col202, col203, col204, col205, col206, col207, col208, col209,
    col210, col211, col212, col213, col214, col215, col216, col217, col218, col219,
    col220)
  CSV DATA ('gs://cea-team/orders/orders.*.csv.gz?AUTH=specified&CREDENTIALS=xxxx')
  WITH delimiter = e'\t', nullif = '' , detached;

