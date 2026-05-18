import os
import random
import logging  # Enterprise standard logging
from datetime import datetime, timedelta
import pandas as pd
import requests
from sqlalchemy import create_engine, types  # Explicit data type binding
from dotenv import load_dotenv

# 1. SETUP ENTERPRISE SYSTEM LOGGING
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("pipeline_execution.log")
    ]
)

load_dotenv()

# 2. SECURITY CHECK
API_KEY = os.getenv("CLIMATIQ_API_KEY")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ENDPOINT = os.getenv("DB_ENDPOINT")

if not all([API_KEY, DB_PASSWORD, DB_ENDPOINT]):
    logging.critical("Environment configuration failed. Missing infrastructure keys.")
    raise EnvironmentError("❌ Critical Failure: Missing required variables in .env file.")

# 3. ROBUST SCHEMA GENERATOR
def generate_enterprise_analytics_data(n=5000):
    logging.info(f"Initiating synthetic generation for {n} enterprise records...")
    materials = ['Steel', 'Aluminum', 'Plastic', 'Copper', 'Glass', 'Iron']
    
    supplier_pool = {
        'China': ['Shagang Group', 'Baosteel', 'Ansteel'],
        'India': ['Tata Steel', 'JSW Steel', 'Hindalco'],
        'Germany': ['Thyssenkrupp', 'BASF Industrial', 'Salzgitter AG'],
        'Sweden': ['SSAB Green', 'Boliden AB', 'Northvolt Materials'],
        'France': ['ArcelorMittal Europe', 'Saint-Gobain', 'Alteo'],
        'USA': ['US Steel', 'Alcoa Corp', 'Freeport-McMoRan'],
        'Vietnam': ['Hoa Phat Group', 'Formosa Ha Tinh'],
        'Brazil': ['Vale S.A.', 'Gerdau', 'Usiminas'],
        'Norway': ['Norsk Hydro', 'Yara International', 'Elkem'],
        'Canada': ['Rio Tinto Can', 'Teck Resources'],
        'Italy': ['Marcegaglia', 'Acciaierie d\'Italia'],
        'Japan': ['Nippon Steel', 'JFE Holdings', 'Kobe Steel']
    }

    rows = []
    base_date = datetime.now()

    for _ in range(n):
        country = random.choice(list(supplier_pool.keys()))
        supplier = random.choice(supplier_pool[country])
        efficiency_modifier = round(random.uniform(0.5, 1.8), 2)
        weight = random.randint(500, 100000)
        material_type = random.choice(materials)
        
        base_price_per_kg = {'Steel': 0.8, 'Aluminum': 2.2, 'Plastic': 1.5, 'Copper': 8.5, 'Glass': 0.4, 'Iron': 0.6}
        calculated_contract_value = int(weight * base_price_per_kg[material_type] * random.uniform(0.9, 1.3))
        
        days_in_future = random.randint(30, 540)
        # Parse directly to a true Python Date object for database conversion safety
        renewal_date = (base_date + timedelta(days=days_in_future)).date()
        
        rows.append({
            'supplier_name': supplier,
            'material_type': material_type,
            'weight_kg': weight,
            'contract_value_usd': calculated_contract_value,
            'supplier_country': country,
            'transport_mode': random.choice(['Ocean', 'Road', 'Air', 'Rail']),
            'supplier_efficiency_score': efficiency_modifier,
            'supplier_tier': random.choice(['Tier 1 (Strategic)', 'Tier 2 (Preferred)', 'Tier 3 (Transactional)']),
            'historical_churn_risk': random.choice(['Low', 'Medium', 'High']),
            'contract_renewal_date': renewal_date,
            'carbon_reduction_target_pct': random.choice([0.10, 0.15, 0.20, 0.25, 0.30])
        })
    return pd.DataFrame(rows)

# 4. API RESILIENCE ENGINE
def get_verified_carbon_factors():
    # UPDATED: Shifted to highly stable, core sector category mapping IDs
    mapping = {
        'Steel': 'metals-type_steel',
        'Aluminum': 'metals-type_aluminium',
        'Plastic': 'plastics_and_rubber_products-type_plastic',
        'Copper': 'metals-type_copper',
        'Glass': 'glass_and_glass_products-type_glass',
        'Iron': 'metals-type_iron'
    }
    fallbacks = {'Steel': 2.3, 'Aluminum': 12.5, 'Plastic': 2.1, 'Copper': 3.8, 'Glass': 1.2, 'Iron': 2.0}
    url = "https://api.climatiq.io/data/v1/estimate"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    factors = {}

    logging.info("Connecting to Climatiq Global Carbon Registry API...")
    for material, activity_id in mapping.items():
        payload = {
            "emission_factor": {"activity_id": activity_id, "data_version": "^3"},
            "parameters": {"weight": 1, "weight_unit": "kg"}
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                factors[material] = response.json()['co2e']
                logging.info(f"Successfully locked API verified factor for {material}: {factors[material]}")
            else:
                logging.warning(f"API HTTP {response.status_code} for {material}. Executing fallback protocol.")
                factors[material] = fallbacks.get(material, 2.5)
        except requests.exceptions.RequestException as e:
            logging.error(f"Network failure mapping {material}: {e}. Initiating default failover backup.")
            factors[material] = fallbacks.get(material, 2.5)
            
    return factors

# --- ORCHESTRATION PIPELINE ---
if __name__ == "__main__":
    logging.info("Starting End-to-End Revenue Intelligence Execution Flow...")
    
    # Extraction
    df = generate_enterprise_analytics_data(5000)
    
    # Enrichment
    api_factors = get_verified_carbon_factors()
    
    # Transformation Layer
    df['carbon_footprint_tonnes'] = (df['weight_kg'] * df['material_type'].map(api_factors) * df['supplier_efficiency_score']) / 1000
    df['carbon_per_usd'] = df['carbon_footprint_tonnes'] / df['contract_value_usd']
    
    high_risk_countries = ['China', 'India', 'Vietnam', 'Brazil']
    df['regulatory_risk_score'] = df.apply(
        lambda x: 'Critical' if x['supplier_country'] in high_risk_countries and x['historical_churn_risk'] == 'High'
                  else ('High' if x['supplier_country'] in high_risk_countries or x['historical_churn_risk'] == 'High' else 'Compliant'), 
        axis=1
    )
    
    # EXPLICIT DATA TYPE STRUCTURING FOR POSTGRES & CRMA
    data_type_schema = {
        'supplier_name': types.VARCHAR(100),
        'material_type': types.VARCHAR(50),
        'weight_kg': types.Integer(),
        'contract_value_usd': types.Integer(),
        'supplier_country': types.VARCHAR(50),
        'transport_mode': types.VARCHAR(20),
        'supplier_efficiency_score': types.Numeric(precision=3, scale=2),
        'supplier_tier': types.VARCHAR(50),
        'historical_churn_risk': types.VARCHAR(20),
        'contract_renewal_date': types.Date(),  # Strictly typed as a structural SQL date
        'carbon_reduction_target_pct': types.Numeric(precision=3, scale=2),
        'carbon_footprint_tonnes': types.Numeric(precision=10, scale=3),
        'carbon_per_usd': types.Numeric(precision=12, scale=6),
        'regulatory_risk_score': types.VARCHAR(20)
    }
    
    # Secure Load Connection 
    connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ENDPOINT}:5432/postgres'
    
    # UPDATED: Standardized SSL connection arguments to seamlessly trust native systems
    ssl_args = {
        "sslmode": "require"
    }
    
    engine = create_engine(connection_string, connect_args=ssl_args)
    
    try:
        logging.info("Opening encrypted tunnel to AWS RDS Instance...")
        df.to_sql(
            'carbon_emissions', 
            engine, 
            if_exists='replace', 
            index=False, 
            dtype=data_type_schema
        )
        logging.info("🏆 SUCCESS: 5,000 highly robust records securely written with full schema enforcement.")
    except Exception as e:
        logging.critical(f"Pipeline broken during database load transaction: {e}")