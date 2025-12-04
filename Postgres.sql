-- DATABASE: ipo_platform

-- Users
CREATE TABLE auth_user (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  full_name VARCHAR(200),
  is_active BOOLEAN DEFAULT TRUE,
  is_staff BOOLEAN DEFAULT FALSE,
  role VARCHAR(20) DEFAULT 'public', -- 'admin' or 'public'
  created_at TIMESTAMP DEFAULT now()
);

-- Companies
CREATE TABLE company (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  ticker VARCHAR(50),
  description TEXT,
  sector VARCHAR(100),
  website VARCHAR(255),
  created_at TIMESTAMP DEFAULT now()
);

-- IPOs
CREATE TABLE ipo (
  id SERIAL PRIMARY KEY,
  company_id INTEGER REFERENCES company(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  issue_start_date DATE,
  issue_end_date DATE,
  listing_date DATE,
  price_band_min NUMERIC(12,2),
  price_band_max NUMERIC(12,2),
  lot_size INTEGER DEFAULT 1,
  total_shares BIGINT,
  exchange VARCHAR(50),
  status VARCHAR(20) DEFAULT 'upcoming', -- upcoming, open, closed, listed
  short_description TEXT,
  created_at TIMESTAMP DEFAULT now()
);

-- Documents
CREATE TABLE document (
  id SERIAL PRIMARY KEY,
  ipo_id INTEGER REFERENCES ipo(id) ON DELETE CASCADE,
  company_id INTEGER REFERENCES company(id) ON DELETE CASCADE,
  title VARCHAR(255),
  file_url TEXT,  -- S3 or local storage path
  is_public BOOLEAN DEFAULT TRUE,
  doc_type VARCHAR(50), -- RHP, DRHP, PROSPECTUS
  created_at TIMESTAMP DEFAULT now()
);

-- Subscriptions
CREATE TABLE subscription (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
  ipo_id INTEGER REFERENCES ipo(id) ON DELETE CASCADE,
  subscribed_at TIMESTAMP DEFAULT now()
);

-- Applications (optional)
CREATE TABLE application (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES auth_user(id),
  ipo_id INTEGER REFERENCES ipo(id),
  bid_amount NUMERIC(14,2),
  quantity INTEGER,
  status VARCHAR(30) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT now()
);

-- Audit Logs
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  actor_id INTEGER REFERENCES auth_user(id),
  entity_type VARCHAR(50),
  entity_id INTEGER,
  action VARCHAR(50),
  details JSONB,
  created_at TIMESTAMP DEFAULT now()
);

-- DUMMY DATA
INSERT INTO auth_user (email, password, full_name, is_staff, role)
VALUES 
('admin@example.com', 'pbkdf2_sha256$216000$dummy$hash', 'Admin User', true,'admin'),
('user1@example.com', 'pbkdf2_sha256$216000$dummy$hash', 'Ranjeet Kumar', false,'public');

INSERT INTO company (name, ticker, description, sector, website)
VALUES ('Example Tech Ltd', 'EXTECH', 'A sample tech company', 'Technology','https://example.com'),
       ('GreenEnergy Inc', 'GREN', 'Renewable energy solutions', 'Energy','https://green.com');

INSERT INTO ipo (company_id, title, issue_start_date, issue_end_date, listing_date, price_band_min, price_band_max, lot_size, total_shares, exchange, status, short_description)
VALUES
(1, 'Example Tech Ltd - IPO', '2026-02-10', '2026-02-12', '2026-02-20', 100.00, 110.00, 10, 5000000, 'NSE', 'upcoming', 'IPO of Example Tech Ltd.'),
(2, 'GreenEnergy Inc - IPO', '2026-01-05', '2026-01-07', '2026-01-15', 50.00, 55.00, 10, 3000000, 'BSE', 'listed', 'Green energy IPO');

INSERT INTO document (ipo_id, company_id, title, file_url, is_public, doc_type)
VALUES
(1,1,'RHP - Example Tech','https://s3.example.com/docs/extech_rhp.pdf', true, 'RHP'),
(2,2,'Prospectus - GreenEnergy','https://s3.example.com/docs/green_prospectus.pdf', true, 'PROSPECTUS');
