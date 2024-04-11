/*
테이블 스키마 조회
SELECT * FROM information_schema.TABLES WHERE table_type='base table' AND TABLE_NAME = 'tb_category'

show tables;

신규 테이블 생성
*/

# 카테고리
DROP TABLE IF EXISTS tb_category;
CREATE TABLE tb_category(
	cate_code TINYINT AUTO_INCREMENT  PRIMARY KEY,
	cate_name VARCHAR(25) NOT NULL,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW());

# 키워드
DROP TABLE IF EXISTS tb_keyword;
CREATE TABLE tb_keyword(
	key_code SMALLINT AUTO_INCREMENT PRIMARY KEY,
	cate_code TINYINT NOT NULL, 
	key_word VARCHAR(50) NOT NULL,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
			
	FOREIGN KEY (cate_code) REFERENCES tb_category(cate_code));

# 관련 뉴스
DROP TABLE IF EXISTS tb_news;
CREATE TABLE tb_news(
	news_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	news_press VARCHAR(50) NOT NULL,
	news_title VARCHAR(100) NOT NULL,
	news_article TEXT NOT NULL,
	write_date DATETIME NOT NULL,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code));

# 기업
DROP TABLE IF EXISTS tb_company;
CREATE TABLE tb_company(
	company_seq INT AUTO_INCREMENT PRIMARY KEY,
	company_name VARCHAR(50) NOT NULL,
	award_yn CHAR(1) DEFAULT '0',
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW());


# 기업 관련 뉴스
DROP TABLE IF EXISTS tb_company_news;
CREATE TABLE tb_company_news(
	news_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	company_seq INT NOT NULL,
	news_press VARCHAR(50) NOT NULL,
	news_title VARCHAR(100) NOT NULL,
	news_article TEXT NOT NULL,
	write_date DATETIME NOT NULL,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));

# 기업 보고서
DROP TABLE IF EXISTS tb_report;
CREATE TABLE tb_report(
	report_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	company_seq INT NOT NULL,
	report_kind VARCHAR(20) NOT NULL,
	rating_year CHAR(4),
	report_name VARCHAR(100) NOT NULL,
	report_content TEXT NOT NULL,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));

# 녹색 제품 현황
DROP TABLE IF EXISTS tb_green_status;
CREATE TABLE tb_green_status(
	green_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	company_seq INT NOT NULL,
	product_name VARCHAR(100) NOT NULL,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));

# 기업 평가
DROP TABLE IF EXISTS tb_esg_rating;
CREATE TABLE tb_esg_rating(
	esg_seq INT AUTO_INCREMENT PRIMARY KEY,
	company_seq INT NOT NULL,
	total_rating VARCHAR(2),
	env_rating VARCHAR(2),
	social_rating VARCHAR(2),
	gov_rating VARCHAR(2),
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));

# 국민 연금 가입
DROP TABLE IF EXISTS tb_nps;
CREATE TABLE tb_nps(
	nps_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	company_seq INT NOT NULL,
	create_year CHAR(10) NOT NULL,
	join_cnt SMALLINT DEFAULT 0,
	new_cnt TINYINT DEFAULT 0,
	loss_cnt TINYINT DEFAULT 0,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));

# 온실 가스 사용량
DROP TABLE IF EXISTS tb_green_gas_status;
CREATE TABLE tb_green_gas_status(
	gas_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	company_seq INT NOT NULL,
	target_year CHAR(4),
	category VARCHAR(10),
	sector VARCHAR(10),
	business_type VARCHAR(100),
	gas_amount INT DEFAULT 0,
	energy_usage INT DEFAULT 0,	
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));

# 폐기물 발생량
DROP TABLE IF EXISTS tb_waste_status;
CREATE TABLE tb_waste_status(
	waste_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	company_seq INT NOT NULL,
	specificity VARCHAR(50),
	business_type VARCHAR(50),
	target_year CHAR(4) NOT NULL,
	total_amount FLOAT DEFAULT 0,	
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));

# 환경성적표지
DROP TABLE IF EXISTS tb_edp;
CREATE TABLE tb_edp(
	edp_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	company_seq INT NOT NULL,
	effect VARCHAR(20) NOT NULL,
	product_type VARCHAR(20) NOT NULL,
	certified VARCHAR(50) NOT NULL,
	carbon_amount FLOAT DEFAULT 0,
	resource_amount FLOAT DEFAULT 0,
	carbon_env_amount FLOAT DEFAULT 0,
	ozone_amount DOUBLE DEFAULT 0,
	acid_amount FLOAT DEFAULT 0,
	nutrients_amount FLOAT DEFAULT 0,
	smog_amount FLOAT DEFAULT 0,
	water_amount FLOAT DEFAULT 0,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));

# 대기오염물질배출시설
DROP TABLE IF EXISTS tb_pollution;
CREATE TABLE tb_pollution(
	pol_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	company_seq INT NOT NULL,
	company_addr VARCHAR(200),
	work_status VARCHAR(10),
	last_update_date CHAR(10),
	dis_work_hour FLOAT DEFAULT 0,
	dis_work_day SMALLINT DEFAULT 0,
	pre_work_hour FLOAT DEFAULT 0,
	pre_work_day SMALLINT DEFAULT 0,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));

# DART 직원 현황
DROP TABLE IF EXISTS tb_dart_employee;
CREATE TABLE tb_dart_employee(
	emp_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	company_seq INT NOT NULL,
	emp_cnt SMALLINT DEFAULT 0,
	regular_cnt SMALLINT DEFAULT 0,
	non_regular_cnt SMALLINT DEFAULT 0,
	salary_total INT DEFAULT 0,
	work_day FLOAT DEFAULT 0,
	work_avg FLOAT DEFAULT 0,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));

# DART 직원 현황
DROP TABLE IF EXISTS tb_dart_director;
CREATE TABLE tb_dart_director(
	director_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	company_seq INT NOT NULL,
	director_cnt SMALLINT DEFAULT 0,
	out_director_cnt SMALLINT DEFAULT 0,
	in_director_cnt SMALLINT DEFAULT 0,
	per_salary_avg FLOAT DEFAULT 0,
	salary_total INT DEFAULT 0,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));

# DART 최대주주 현황
DROP TABLE IF EXISTS tb_dart_stock;
CREATE TABLE tb_dart_stock(
	stock_seq INT AUTO_INCREMENT PRIMARY KEY,
	key_code SMALLINT NOT NULL,
	company_seq INT NOT NULL,
	top_stock_percent FLOAT DEFAULT 0,
	create_date DATETIME DEFAULT NOW(),
	update_date DATETIME DEFAULT NOW(),
	
	FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
	FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));