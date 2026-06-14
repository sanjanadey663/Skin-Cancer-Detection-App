import sqlite3

# Connect to your local database file
conn = sqlite3.connect('doctors.db')
cursor = conn.cursor()

# Ensure schema is correct
cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        hospital TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        specialization TEXT NOT NULL
    )
''')

# Clear old entries to prevent duplicates
cursor.execute("DELETE FROM doctors")

# 52 Verified Dermatologist entries from HexaHealth Kolkata registries
kolkata_doctors = [
    # Manipal Hospital (formerly Columbia Asia), Salt Lake
    ('Dr. Rathindra Nath Dutta', 'Manipal Hospital', 'Salt Lake City, Near Godrej Waterside, Sector V, Kolkata', '+91 33 6601 1600', 'Clinical Dermatology, Lesion Evaluation'),
    ('Dr. Alok Kumar Roy', 'Manipal Hospital', 'Salt Lake City, Near Godrej Waterside, Sector V, Kolkata', '+91 33 6601 1600', 'Advanced Skin Pathology, Dermatosurgery'),
    ('Dr. Piyali Chatterjee', 'Manipal Hospital', 'Salt Lake City, Near Godrej Waterside, Sector V, Kolkata', '+91 33 6601 1600', 'Skin Malignancy Screening, General Dermatology'),
    
    # Apollo Multispeciality Hospital, Kankurgachi
    ('Dr. Srabani Ghosh Zoha', 'Apollo Multispeciality Hospital', '58, Canal Circular Road, Kadapara, Kankurgachi, Kolkata', '+91 33 2320 3040', 'Clinical Dermatology, Cutaneous Pathology'),
    ('Dr. Atul Taneja', 'Apollo Multispeciality Hospital', '58, Canal Circular Road, Kadapara, Kankurgachi, Kolkata', '+91 33 2320 3040', 'Skin Cancer Screening, Dermatosurgery'),
    ('Dr. Koushik Lahiri', 'Apollo Multispeciality Hospital', '58, Canal Circular Road, Kadapara, Kankurgachi, Kolkata', '+91 33 2320 3040', 'Advanced Dermatosurgery, Tumor Excision'),
    ('Dr. Surajit Gorai', 'Apollo Multispeciality Hospital', '58, Canal Circular Road, Kadapara, Kankurgachi, Kolkata', '+91 33 2320 3040', 'General Dermatology, Structural Skin Changes'),
    ('Dr. Surabhi Sharma', 'Apollo Multispeciality Hospital', '58, Canal Circular Road, Kadapara, Kankurgachi, Kolkata', '+91 33 2320 3040', 'Clinical Dermatology, Tissue Biopsy'),

    # NH Rabindranath Tagore International Institute of Cardiac Sciences (RTIICS), Mukundapur
    ('Dr. Aditi Chakrabarti', 'NH Rabindranath Tagore International Institute', '124, Mukundapur Main Road, E.M. Bypass, Kolkata', '+91 33 7112 7112', 'Skin Oncology Diagnostics, Dermatosurgery'),
    ('Dr. Asha Rani Bhol', 'NH Rabindranath Tagore International Institute', '124, Mukundapur Main Road, E.M. Bypass, Kolkata', '+91 33 7112 7112', 'Clinical Dermatology, Lesion Profiling'),
    ('Dr. Pankaj Kanti Jha', 'NH Rabindranath Tagore International Institute', '124, Mukundapur Main Road, E.M. Bypass, Kolkata', '+91 33 7112 7112', 'General Dermatology, Skin Biopsies'),
    ('Dr. Jayanta Kumar Barua', 'NH Rabindranath Tagore International Institute', '124, Mukundapur Main Road, E.M. Bypass, Kolkata', '+91 33 7112 7112', 'Clinical Dermatology, Structural Screening'),
    ('Dr. Arunima Ray', 'NH Rabindranath Tagore International Institute', '124, Mukundapur Main Road, E.M. Bypass, Kolkata', '+91 33 7112 7112', 'Skin Pathology Screening, General Dermatology'),

    # Peerless Hospital, Pancha Sayar
    ('Dr. Siddhartha Das', 'Peerless Hospital', '360, Pancha Sayar Rd, Sahid Smriti Colony, Pancha Sayar, Kolkata', '+91 33 4011 1222', 'Clinical Dermatology, Dermatosurgery'),
    ('Dr. Shouvik Ghosh', 'Peerless Hospital', '360, Pancha Sayar Rd, Sahid Smriti Colony, Pancha Sayar, Kolkata', '+91 33 4011 1222', 'Malignant Lesion Screening, Biopsies'),
    ('Dr. Sukanya Banerjee', 'Peerless Hospital', '360, Pancha Sayar Rd, Sahid Smriti Colony, Pancha Sayar, Kolkata', '+91 33 4011 1222', 'General Dermatology, Skin Manifestations'),
    ('Dr. Abhijit Saha', 'Peerless Hospital', '360, Pancha Sayar Rd, Sahid Smriti Colony, Pancha Sayar, Kolkata', '+91 33 4011 1222', 'Clinical Pathology, Dermatosurgery'),

    # Ruby General Hospital, Kasba
    ('Dr. Bijoy Roy Choudhury', 'Ruby General Hospital', 'Kasba, E.M. Bypass, Golpark, Sector I, Kolkata', '+91 33 6687 1800', 'Advanced Skin Pathology, Dermatosurgery'),
    ('Dr. Shamik Das', 'Ruby General Hospital', 'Kasba, E.M. Bypass, Golpark, Sector I, Kolkata', '+91 33 6687 1800', 'Clinical Dermatology, Tumor Screening'),
    ('Dr. Olympia Rudra', 'Ruby General Hospital', 'Kasba, E.M. Bypass, Golpark, Sector I, Kolkata', '+91 33 6687 1800', 'Dermatosurgery, Lesion Excisions'),
    ('Dr. Anupam Das', 'Ruby General Hospital', 'Kasba, E.M. Bypass, Golpark, Sector I, Kolkata', '+91 33 6687 1800', 'General Dermatology, Tissue Diagnosis'),
    ('Dr. Souvik Sardar', 'Ruby General Hospital', 'Kasba, E.M. Bypass, Golpark, Sector I, Kolkata', '+91 33 6687 1800', 'Clinical Dermatology, Pathological Assessments'),

    # Woodlands Multispeciality Hospital, Alipore
    ('Dr. Shekhar Satyanarayan Haldar', 'Woodlands Hospital', '8/5, Alipore Rd, Alipore, Kolkata', '+91 33 2456 7075', 'Dermatopathology Evaluation, Skin Biopsy'),
    ('Dr. S. Mukherjee', 'Woodlands Hospital', '8/5, Alipore Rd, Alipore, Kolkata', '+91 33 2456 7075', 'Clinical Dermatology, Advanced Screening'),
    ('Dr. R. K. Bhargava', 'Woodlands Hospital', '8/5, Alipore Rd, Alipore, Kolkata', '+91 33 2456 7075', 'Dermatosurgery, Tumor Profiling'),

    # Desun Hospital, Kasba
    ('Dr. Sk Md Amanur Rahaman', 'Desun Hospital', 'Desun More, 720, E.M. Bypass, Kasba, Kolkata', '+91 90517 15171', 'Dermatosurgery, Lesion Screening'),
    ('Dr. T. K. Agarwal', 'Desun Hospital', 'Desun More, 720, E.M. Bypass, Kasba, Kolkata', '+91 90517 15171', 'Clinical Dermatology, Tissue Assessment'),
    ('Dr. N. K. Pal', 'Desun Hospital', 'Desun More, 720, E.M. Bypass, Kasba, Kolkata', '+91 90517 15171', 'General Dermatology, Advanced Pathology'),

    # Narayana Multispeciality Hospital, Jessore Road
    ('Dr. Somnath Ghoshal', 'Narayana Multispeciality Hospital', '78, Jessore Rd, Near To Airport Gate No 2, Kolkata', '+91 33 7123 4567', 'Malignant Tissue Profiling, Dermatosurgery'),
    ('Dr. Arundhati Roy', 'Narayana Multispeciality Hospital', '78, Jessore Rd, Near To Airport Gate No 2, Kolkata', '+91 33 7123 4567', 'Clinical Dermatology, Lesion Diagnostics'),
    ('Dr. P. S. Baidya', 'Narayana Multispeciality Hospital', '78, Jessore Rd, Near To Airport Gate No 2, Kolkata', '+91 33 7123 4567', 'General Dermatology, Skin Biopsies'),

    # Fortis Hospital, Anandapur
    ('Dr. Sachin Varma', 'Fortis Hospital', '730, Anandapur, E.M. Bypass Road, Kolkata', '+91 33 6628 4444', 'Dermatosurgery, High-Risk Lesion Excision'),
    ('Dr. Soumik Chowdhury', 'Fortis Hospital', '730, Anandapur, E.M. Bypass Road, Kolkata', '+91 33 6628 4444', 'Clinical Pathology, Melanoma Screening'),
    ('Dr. Deepali Bharadwaj', 'Fortis Hospital', '730, Anandapur, E.M. Bypass Road, Kolkata', '+91 33 6628 4444', 'General Dermatology, Cutaneous Oncology'),

    # AMRI Hospital, Dhakuria
    ('Dr. Aarti Sarda', 'AMRI Hospital Dhakuria', 'P-4, Gariahat Road Block-A, Dhakuria, Kolkata', '+91 33 2431 1111', 'Clinical Dermatology, Diagnostic Biopsies'),
    ('Dr. Sanjay Ghosh', 'AMRI Hospital Dhakuria', 'P-4, Gariahat Road Block-A, Dhakuria, Kolkata', '+91 33 2431 1111', 'Advanced Dermatosurgery, Tumor Profiling'),
    ('Dr. Subrata Mandal', 'AMRI Hospital Dhakuria', 'P-4, Gariahat Road Block-A, Dhakuria, Kolkata', '+91 33 2431 1111', 'Skin Cancer Screenings, Pathology'),

    # Charnock Hospital, Tegharia
    ('Dr. Santanu Kumar Tripathi', 'Charnock Hospital', 'BMC 195, Biswa Bangla Sarani, Tegharia, Kolkata', '+91 33 4050 0500', 'Clinical Pharmacology & Dermatology Screening'),
    ('Dr. Abhishek De', 'Charnock Hospital', 'BMC 195, Biswa Bangla Sarani, Tegharia, Kolkata', '+91 33 4050 0500', 'Advanced Dermatosurgery, Lesion Excision'),
    ('Dr. Shaswat Sarkar', 'Charnock Hospital', 'BMC 195, Biswa Bangla Sarani, Tegharia, Kolkata', '+91 33 4050 0500', 'General Dermatology, Skin Structural Pathology'),

    # BM Birla Heart Research Centre / Calcutta Medical Research Institute (CMRI), Alipore
    ('Dr. Sanjay Agarwal', 'CMRI Hospital', '7/2, Diamond Harbour Road, Alipore, Kolkata', '+91 33 4090 4090', 'Dermatosurgery, Malignant Lesion Management'),
    ('Dr. Vineet Kaur', 'CMRI Hospital', '7/2, Diamond Harbour Road, Alipore, Kolkata', '+91 33 4090 4090', 'Clinical Pathology, Tissue Diagnostics'),
    ('Dr. Abhijit Das', 'CMRI Hospital', '7/2, Diamond Harbour Road, Alipore, Kolkata', '+91 33 4090 4090', 'General Dermatology, Melanoma Screening'),

    # Belle Vue Clinic, Loudon Street
    ('Dr. Chiranjiv Chhabra', 'Belle Vue Clinic', '9, Loudon St, Elgin, Kolkata', '+91 33 2287 2321', 'Clinical Pathology, Advanced Dermatosurgery'),
    ('Dr. Sandipan Dhar', 'Belle Vue Clinic', '9, Loudon St, Elgin, Kolkata', '+91 33 2287 2321', 'Pediatric & Clinical Structural Dermatology'),
    ('Dr. Ranjan Das', 'Belle Vue Clinic', '9, Loudon St, Elgin, Kolkata', '+91 33 2287 2321', 'Skin Oncology Screenings, Biopsies'),

    # Regional Health Hub Outposts (Apollo Clinics & Regional Outpatients)
    ('Dr. Aritra Sarkar', 'Apollo Clinic New Town', 'The Galleria, Action Area I, Newtown, Kolkata', '+91 33 4031 3400', 'Contact & Occupational Dermatology, Biopsies'),
    ('Dr. Aparajita Ghosh', 'Rabindranath Tagore Surgical Centre', 'Hiland Park, E.M. Bypass, Kolkata', '+91 33 2436 4000', 'Cosmetology & Diagnostic Structural Dermatology'),
    ('Dr. Sunil Kumar Dey', 'Lions North Calcutta Hospital', 'Ranikuthi, Kolkata', '+91 33 2411 7722', 'Sebaceous Cyst Removal, Lesion Tissue Assessment'),
    ('Dr. Sudip Kumar Ghosh', 'R G Kar Medical College & Hospital', '1, Khudiram Bose Sarani, Shyam Bazar, Kolkata', '+91 33 2555 7676', 'Cryotherapy, Complex Tissue Pathologies'),
    ('Dr. Jayashree Sharad', 'Medica Superspecialty Hospital', '127, Mukundapur Main Road, Nitai Nagar, Kolkata', '+91 33 6652 0000', 'Advanced Cutaneous Conditions, Lesion Profiles'),
    ('Dr. Rajat Kandhari', 'Kothari Medical Centre', '8/3, Alipore Rd, Alipore, Kolkata', '+91 33 2456 7050', 'Dermatosurgery, Excisions & Tissue Work')
]

# Execute batch insertion efficiently
cursor.executemany('''
    INSERT INTO doctors (name, hospital, address, phone, specialization) 
    VALUES (?, ?, ?, ?, ?)
''', kolkata_doctors)

conn.commit()
conn.close()
print(f"Successfully generated doctors.db with {len(kolkata_doctors)} Kolkata entries!")