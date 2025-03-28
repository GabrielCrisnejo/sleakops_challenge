CREATE TABLE pricing_data (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(255) UNIQUE NOT NULL,
    product_family VARCHAR(255),
    database_engine VARCHAR(255),
    instance_type VARCHAR(255),
    memory VARCHAR(255),
    vcpu INTEGER
);

CREATE TABLE terms (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(255) REFERENCES pricing_data(sku),
    offerTermCode VARCHAR(255),
    effectiveDate TIMESTAMP,
    termType VARCHAR(50),
    leaseContractLength VARCHAR(50),
    purchaseOption VARCHAR(50)
);

CREATE TABLE price_dimensions (
    id SERIAL PRIMARY KEY,
    term_id INTEGER REFERENCES terms(id),
    rateCode VARCHAR(255),
    unit VARCHAR(50),
    beginRange NUMERIC,
    endRange VARCHAR(20),
    description TEXT,
    priceUSD NUMERIC
);