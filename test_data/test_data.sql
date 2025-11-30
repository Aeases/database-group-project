-- ============================================
-- EMPLOYEE TABLE
-- ============================================
INSERT INTO EMPLOYEE (e_name, e_phone, e_email, supervisor_id, level) VALUES 
('John Arbuckle', '61929507', 'john.arbuckle@university.edu', NULL, 'executive officer'),
('Skibidi Sigma', '22712679', 'skibidi.sigma@university.edu', 1, 'mid-level manager'),
('Garfield Rizz', '37058588', 'garfield.rizz@university.edu', 1, 'mid-level manager'),
('Quandale Fortnite', '52523057', 'quandale.fortnight@university.edu', 2, 'base-level worker'),
('Usagi Rabbit', '36452595', 'usagi.rabbit@university.edu', 3, 'base-level worker');

-- ============================================
-- CMM_ACTIVITY TABLE
-- ============================================
INSERT INTO CMM_ACTIVITY (activity_desc, start_date, end_date, makes_unusable, category) VALUES 
('window cleaning', '2025-11-25', '2025-11-26', 1, 'cleaning'),
('floor cleaning', '2025-11-27', '2025-11-28', 0, 'cleaning'),
('door repair', '2025-11-29', '2025-11-30', 1, 'repair'),
('leak repair', '2025-12-01', '2025-12-02', 1, 'repair'),
('speaker repair', '2025-12-03', '2025-12-04', 1, 'repair');

-- ============================================
-- SUBCONTRACTOR TABLE
-- ============================================
INSERT INTO SUBCONTRACTOR (c_name, c_phone, c_email) VALUES 
('Hachiware Musk', '34671097', 'hachiwaremusk@gmail.com'),
('Elon Ma', '56846438', 'elonma@outlook.com');

-- ============================================
-- E_ASSIGNMENT TABLE (Employee Assignments)
-- ============================================
INSERT INTO E_ASSIGNMENT (a_id, e_id) VALUES 
(1, 3),   -- window cleaning -> Garfield Rizz
(2, 5),   -- floor cleaning -> Usagi Rabbit
(3, 4);   -- door repair -> Quandale Fortnite

-- ============================================
-- C_ASSIGNMENT TABLE (Subcontractor Assignments)
-- ============================================
INSERT INTO C_ASSIGNMENT (a_id, c_id) VALUES 
(2, 1),   -- floor cleaning -> Hachiware Musk
(5, 2);   -- speaker repair -> Elon Ma

-- ============================================
-- CAMPUS_AREA TABLE
-- ============================================
INSERT INTO CAMPUS_AREA (area_id, area_name, area_type, last_maintenance_date) VALUES 
(1, 'R508', 'room', '2025-11-25'),
(2, 'Communal Building', 'building', '2025-11-17'),
(3, 'Y3', 'level', '2025-11-18');

-- ============================================
-- ACTIVITY_LOCATIONS TABLE
-- ============================================
INSERT INTO ACTIVITY_LOCATIONS (location_id, a_id) VALUES 
(1, 2),   -- R508 for floor cleaning
(2, 1),   -- Communal Building for window cleaning
(2, 3),   -- Communal Building for door repair
(3, 4),   -- Y3 for leak repair
(2, 5);   -- Communal Building for speaker repair

-- ============================================
-- CHEMICALS TABLE
-- ============================================
INSERT INTO CHEMICALS (chemical_id, chemical_name, is_harmful) VALUES 
(1, 'windex', 1),
(2, 'soap mix', 0),
(3, 'degreaser', 1),
(4, 'lubricant oil', 0);

-- ============================================
-- CHEMICAL_USAGE TABLE
-- ============================================
INSERT INTO CHEMICAL_USAGE (chemical_id, a_id) VALUES 
(1, 1),   -- windex for window cleaning
(2, 2),   -- soap mix for floor cleaning
(4, 3);   -- lubricant oil for door repair

-- ============================================
-- BUILDING_SUPERVISION TABLE
-- ============================================
INSERT INTO BUILDING_SUPERVISION (building_id, e_id) VALUES 
(2, 3);   -- Communal Building -> Garfield Rizz
