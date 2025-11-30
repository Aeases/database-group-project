-- ============================================
-- CAMPUS_AREA TABLE
-- ============================================

-- Buildings
INSERT INTO CAMPUS_AREA (area_name, area_type, last_maintenance_date) VALUES 
('Core A', 'building', '2025-09-15'),
('Core B', 'building', '2025-10-20'),
('Core C', 'building', '2025-08-05'),
('Core D', 'building', '2025-11-12'),
('Core E', 'building', '2025-07-28'),
('Core F', 'building', '2025-10-08'),
('Core G', 'building', '2025-09-30'),
('Core H', 'building', '2025-08-22'),
('Core J', 'building', '2025-11-05'),
('Block L', 'building', '2025-10-15'),
('Block M', 'building', '2025-09-08'),
('Block N', 'building', '2025-08-18'),
('Core P', 'building', '2025-10-25'),
('Core P ACL', 'building', '2025-09-12'),
('Core P HOI', 'building', '2025-11-02'),
('Core Q', 'building', '2025-08-30'),
('Core R', 'building', '2025-10-10'),
('Core S', 'building', '2025-09-25'),
('Core S Comm', 'building', '2025-11-08'),
('Core T', 'building', '2025-08-14'),
('Core U', 'building', '2025-10-28'),
('Block V', 'building', '2025-09-18'),
('Block VA', 'building', '2025-11-12'),
('Block VS', 'building', '2025-08-26'),
('Block W', 'building', '2025-10-05'),
('Block W IC', 'building', '2025-09-22'),
('Block X', 'building', '2025-11-15'),
('Block Y', 'building', '2025-08-08'),
('Block Z', 'building', '2025-10-18'),
('Jockey Aud', 'building', '2025-09-28');

-- Generate levels and rooms for each building
-- Core A levels
INSERT INTO CAMPUS_AREA (area_name, area_type, last_maintenance_date) VALUES 
('A1', 'level', '2025-09-10'), ('A2', 'level', '2025-09-12'), ('A3', 'level', '2025-09-08'),
-- Core A rooms
('A101', 'room', '2025-08-15'), ('A102', 'room', '2025-08-20'), ('A103', 'room', '2025-08-18'), ('A104', 'room', '2025-08-22'), ('A105', 'room', '2025-08-25'),
('A201', 'room', '2025-09-05'), ('A202', 'room', '2025-09-08'), ('A203', 'room', '2025-09-02'), ('A204', 'room', '2025-09-10'), ('A205', 'room', '2025-09-12'),
('A301', 'room', '2025-08-28'), ('A302', 'room', '2025-08-30'), ('A303', 'room', '2025-09-01'), ('A304', 'room', '2025-08-26'), ('A305', 'room', '2025-08-24');

-- Core B levels and rooms (similar pattern for all buildings)
INSERT INTO CAMPUS_AREA (area_name, area_type, last_maintenance_date) VALUES 
('B1', 'level', '2025-10-15'), ('B2', 'level', '2025-10-18'), ('B3', 'level', '2025-10-12'),
('B101', 'room', '2025-09-20'), ('B102', 'room', '2025-09-22'), ('B103', 'room', '2025-09-25'), ('B104', 'room', '2025-09-18'), ('B105', 'room', '2025-09-28'),
('B201', 'room', '2025-10-05'), ('B202', 'room', '2025-10-08'), ('B203', 'room', '2025-10-02'), ('B204', 'room', '2025-10-10'), ('B205', 'room', '2025-10-12'),
('B301', 'room', '2025-09-30'), ('B302', 'room', '2025-10-01'), ('B303', 'room', '2025-09-26'), ('B304', 'room', '2025-10-03'), ('B305', 'room', '2025-09-28');

-- Gates
INSERT INTO CAMPUS_AREA (area_name, area_type, last_maintenance_date) VALUES 
('Podium Gate', 'gate', '2025-10-20'),
('Main Gate', 'gate', '2025-11-05'),
('Carpark Gate', 'gate', '2025-09-15'),
('Block Z Gate', 'gate', '2025-10-28');

-- Squares
INSERT INTO CAMPUS_AREA (area_name, area_type, last_maintenance_date) VALUES 
('Logo Square', 'square', '2025-09-25'),
('University Sq', 'square', '2025-10-30'),
('Memorial Sq', 'square', '2025-08-18'),
('Fountain Sq', 'square', '2025-11-08');

-- ============================================
-- SUBCONTRACTOR TABLE (10 companies)
-- ============================================
INSERT INTO SUBCONTRACTOR (c_name, c_phone, c_email) VALUES 
('Elite Maintenance Co.', '25678901', 'contact@elitemaintenance.com'),
('Precision Cleaners Ltd.', '28765432', 'info@precisioncleaners.hk'),
('Urban Facilities Group', '23456789', 'service@urbanfacilities.com'),
('Apex Building Services', '29876543', 'admin@apexbuildings.com'),
('Metro Clean Solutions', '27654321', 'operations@metroclean.hk'),
('Prime Contractors Intl', '26543210', 'projects@primecontractors.com'),
('Cityscape Maintenance', '28901234', 'support@cityscapemaint.com'),
('Professional Care Ltd.', '25789012', 'team@procareltd.hk'),
('Building Works Co.', '26789013', 'work@buildingworks.com'),
('Facility Masters Group', '27890124', 'contact@facilitymasters.hk');

-- ============================================
-- EMPLOYEE TABLE (100 employees)
-- ============================================

-- Executive Officer (1)
INSERT INTO EMPLOYEE (e_name, e_phone, e_email, supervisor_id, level) VALUES 
('Dr. Michael Chen', '61234567', 'michael.chen@university.edu', NULL, 'executive officer');

-- Mid-level Managers (20)
INSERT INTO EMPLOYEE (e_name, e_phone, e_email, supervisor_id, level) VALUES 
('Sarah Wong', '62345678', 'sarah.wong@university.edu', 1, 'mid-level manager'),
('David Li', '63456789', 'david.li@university.edu', 1, 'mid-level manager'),
('Jennifer Zhang', '64567890', 'jennifer.zhang@university.edu', 1, 'mid-level manager'),
('Kevin Tsang', '65678901', 'kevin.tsang@university.edu', 1, 'mid-level manager'),
('Amy Lau', '66789012', 'amy.lau@university.edu', 1, 'mid-level manager'),
('Brian Cheung', '67890123', 'brian.cheung@university.edu', 1, 'mid-level manager'),
('Michelle Ho', '68901234', 'michelle.ho@university.edu', 1, 'mid-level manager'),
('Alex Ng', '69012345', 'alex.ng@university.edu', 1, 'mid-level manager'),
('Grace Mak', '60123456', 'grace.mak@university.edu', 1, 'mid-level manager'),
('Victor Lam', '61234568', 'victor.lam@university.edu', 1, 'mid-level manager'),
('Catherine Yip', '62345679', 'catherine.yip@university.edu', 1, 'mid-level manager'),
('Samuel Chan', '63456780', 'samuel.chan@university.edu', 1, 'mid-level manager'),
('Olivia Poon', '64567891', 'olivia.poon@university.edu', 1, 'mid-level manager'),
('Daniel Wu', '65678902', 'daniel.wu@university.edu', 1, 'mid-level manager'),
('Emily Tang', '66789013', 'emily.tang@university.edu', 1, 'mid-level manager'),
('Henry Yu', '67890124', 'henry.yu@university.edu', 1, 'mid-level manager'),
('Jessica Leung', '68901235', 'jessica.leung@university.edu', 1, 'mid-level manager'),
('Peter Mok', '69012346', 'peter.mok@university.edu', 1, 'mid-level manager'),
('Vanessa Sit', '60123457', 'vanessa.sit@university.edu', 1, 'mid-level manager'),
('Raymond Fong', '61234569', 'raymond.fong@university.edu', 1, 'mid-level manager'),
('Benny Cheng', '62345682', 'benny.cheng@university.edu', 12, 'base-level worker'),
('Gloria Poon', '63456783', 'gloria.poon@university.edu', 12, 'base-level worker'),
('Harry Yeung', '64567894', 'harry.yeung@university.edu', 13, 'base-level worker'),
('Iris Choi', '65678905', 'iris.choi@university.edu', 13, 'base-level worker'),
('Jacky Tang', '66789016', 'jacky.tang@university.edu', 14, 'base-level worker'),
('Kelly Wong', '67890127', 'kelly.wong@university.edu', 14, 'base-level worker'),
('Lawrence Szeto', '68901238', 'lawrence.szeto@university.edu', 15, 'base-level worker'),
('Mona Chan', '69012349', 'mona.chan@university.edu', 15, 'base-level worker'),
('Nathan Cheung', '60123460', 'nathan.cheung@university.edu', 16, 'base-level worker'),
('Ophelia Ho', '61234572', 'ophelia.ho@university.edu', 16, 'base-level worker'),
('Patrick Lam', '62345683', 'patrick.lam@university.edu', 17, 'base-level worker'),
('Queena Ng', '63456784', 'queena.ng@university.edu', 17, 'base-level worker'),
('Ryan Mok', '64567895', 'ryan.mok@university.edu', 18, 'base-level worker'),
('Sandy Yip', '65678906', 'sandy.yip@university.edu', 18, 'base-level worker'),
('Terry Fong', '66789017', 'terry.fong@university.edu', 19, 'base-level worker'),
('Una Leung', '67890128', 'una.leung@university.edu', 19, 'base-level worker'),
('Vincent Yu', '68901239', 'vincent.yu@university.edu', 20, 'base-level worker'),
('Winnie Sit', '69012350', 'winnie.sit@university.edu', 20, 'base-level worker'),
('Xavier Wu', '60123461', 'xavier.wu@university.edu', 2, 'base-level worker'),
('Yvonne Zhang', '61234573', 'yvonne.zhang@university.edu', 2, 'base-level worker'),
('Zack Lau', '62345684', 'zack.lau@university.edu', 3, 'base-level worker'),
('Alice Tsang', '63456785', 'alice.tsang@university.edu', 3, 'base-level worker'),
('Bobby Mak', '64567896', 'bobby.mak@university.edu', 4, 'base-level worker'),
('Catherine Poon', '65678907', 'catherine.poon@university.edu', 4, 'base-level worker'),
('Dennis Yuen', '66789018', 'dennis.yuen@university.edu', 5, 'base-level worker'),
('Eva Hui', '67890129', 'eva.hui@university.edu', 5, 'base-level worker'),
('Felix Kong', '68901240', 'felix.kong@university.edu', 6, 'base-level worker'),
('Gigi Man', '69012351', 'gigi.man@university.edu', 6, 'base-level worker'),
('Howard Pang', '60123462', 'howard.pang@university.edu', 7, 'base-level worker'),
('Irene So', '61234574', 'irene.so@university.edu', 7, 'base-level worker'),
('Justin Tam', '62345685', 'justin.tam@university.edu', 8, 'base-level worker'),
('Katherine Wan', '63456786', 'katherine.wan@university.edu', 8, 'base-level worker'),
('Leo Shum', '64567897', 'leo.shum@university.edu', 9, 'base-level worker'),
('Megan To', '65678908', 'megan.to@university.edu', 9, 'base-level worker'),
('Norman Hung', '66789019', 'norman.hung@university.edu', 10, 'base-level worker'),
('Olivia Kwan', '67890130', 'olivia.kwan@university.edu', 10, 'base-level worker'),
('Peter Cheng', '68901241', 'peter.cheng@university.edu', 11, 'base-level worker'),
('Queenie Poon', '69012352', 'queenie.poon@university.edu', 11, 'base-level worker'),
('Raymond Yeung', '60123463', 'raymond.yeung@university.edu', 12, 'base-level worker'),
('Samantha Choi', '61234575', 'samantha.choi@university.edu', 12, 'base-level worker'),
('Thomas Tang', '62345686', 'thomas.tang@university.edu', 13, 'base-level worker'),
('Ursula Wong', '63456787', 'ursula.wong@university.edu', 13, 'base-level worker'),
('Victor Szeto', '64567898', 'victor.szeto@university.edu', 14, 'base-level worker'),
('Wendy Chan', '65678909', 'wendy.chan@university.edu', 14, 'base-level worker'),
('Xander Cheung', '66789020', 'xander.cheung@university.edu', 15, 'base-level worker'),
('Yolanda Ho', '67890131', 'yolanda.ho@university.edu', 15, 'base-level worker'),
('Zane Lam', '68901242', 'zane.lam@university.edu', 16, 'base-level worker'),
('Abby Ng', '69012353', 'abby.ng@university.edu', 16, 'base-level worker'),
('Brian Mok', '60123464', 'brian.mok@university.edu', 17, 'base-level worker'),
('Coco Yip', '61234576', 'coco.yip@university.edu', 17, 'base-level worker'),
('Darren Fong', '62345687', 'darren.fong@university.edu', 18, 'base-level worker'),
('Elaine Leung', '63456788', 'elaine.leung@university.edu', 18, 'base-level worker'),
('Freddie Yu', '64567899', 'freddie.yu@university.edu', 19, 'base-level worker'),
('Grace Sit', '65678910', 'grace.sit@university.edu', 19, 'base-level worker'),
('Henry Wu', '66789021', 'henry.wu@university.edu', 20, 'base-level worker'),
('Skibidi Sigma', '67890132', 'skibidi.sigma@university.edu', 20, 'base-level worker'),
('Garfield Rizz', '68901243', 'garfield.rizz@university.edu', 2, 'base-level worker'),
('Quandale Fortnite', '69012354', 'quandale.fortnite@university.edu', 3, 'base-level worker'),
('Usage Rabbit', '60123465', 'usagi.rabbit@university.edu', 4, 'base-level worker');
-- ============================================
-- CHEMICALS TABLE (15 specific products)
-- ============================================
INSERT INTO CHEMICALS (chemical_name, is_harmful) VALUES 
('Clorox Clean-Up', 1),
('Lysol Disinfectant', 1),
('Simple Green Pro', 0),
('Goo Gone Pro', 1),
('WD-40 Specialist', 1),
('Krud Kutter Original', 0),
('Zep Heavy-Duty Degreaser', 1),
('Fantastik All-Purpose', 0),
('409 All Surface Cleaner', 0),
('Windex Multi-Surface', 0),
('Tide Professional Clean', 0),
('Comet Disinfectant', 1),
('Pine-Sol Original', 1),
('Mean Green Degreaser', 1),
('Fabuloso Multi-Purpose', 0);

-- ============================================
-- CMM_ACTIVITY TABLE (30 diverse activities)
-- ============================================
INSERT INTO CMM_ACTIVITY (activity_desc, start_date, end_date, makes_unusable, category) VALUES 
('Window cleaning - Core A exterior', '2025-11-25', '2025-11-26', 1, 'cleaning'),
('Floor polishing - Main lobby', '2025-11-27', '2025-11-28', 0, 'cleaning'),
('Door mechanism repair - Block L', '2025-11-29', '2025-11-30', 1, 'repair'),
('Water leak repair - Core C washrooms', '2025-12-01', '2025-12-02', 1, 'repair'),
('Speaker system upgrade - Auditorium', '2025-12-03', '2025-12-04', 1, 'renovation'),
('HVAC maintenance - Core P', '2025-12-05', '2025-12-06', 0, 'repair'),
('Carpet deep cleaning - Admin offices', '2025-12-07', '2025-12-08', 1, 'cleaning'),
('Lighting system retrofit - Library', '2025-12-09', '2025-12-10', 1, 'renovation'),
('Elevator modernization - Block M', '2025-12-11', '2025-12-15', 1, 'renovation'),
('Restroom renovation - Core S', '2025-12-16', '2025-12-20', 1, 'renovation'),
('Exterior painting - Core B facade', '2025-12-21', '2025-12-24', 0, 'repair'),
('Floor tile replacement - Cafeteria', '2025-12-25', '2025-12-28', 1, 'repair'),
('Electrical panel upgrade - Core D', '2025-12-29', '2025-12-31', 1, 'renovation'),
('Pest control treatment - All buildings', '2026-01-02', '2026-01-03', 0, 'cleaning'),
('Fountain pump repair - Fountain Square', '2026-01-04', '2026-01-05', 1, 'repair'),
('Gate automation install - Main Gate', '2026-01-06', '2026-01-07', 1, 'renovation'),
('Wall repainting - Student lounges', '2026-01-08', '2026-01-10', 0, 'repair'),
('Floor waxing - Corridors Level 2', '2026-01-11', '2026-01-12', 0, 'cleaning'),
('Window seal replacement - Core F', '2026-01-13', '2026-01-14', 1, 'repair'),
('Data cabling install - Computer labs', '2026-01-15', '2026-01-17', 1, 'renovation'),
('Ceiling tile replacement - Lecture halls', '2026-01-18', '2026-01-19', 1, 'repair'),
('Graffiti removal - External walls', '2026-01-20', '2026-01-21', 0, 'cleaning'),
('Fire system inspection - All buildings', '2026-01-22', '2026-01-24', 0, 'repair'),
('Landscape maintenance - University Sq', '2026-01-25', '2026-01-26', 0, 'cleaning'),
('Furniture assembly - New classrooms', '2026-01-27', '2026-01-28', 1, 'renovation'),
('Water filter replacement - All floors', '2026-01-29', '2026-01-30', 0, 'repair'),
('Signage installation - Wayfinding', '2026-01-31', '2026-02-01', 0, 'renovation'),
('Floor mat cleaning - Entrances', '2026-02-02', '2026-02-03', 0, 'cleaning'),
('Whiteboard replacement - Classrooms', '2026-02-04', '2026-02-05', 1, 'repair'),
('Security camera install - Perimeter', '2026-02-06', '2026-02-08', 1, 'renovation');

-- ============================================
-- E_ASSIGNMENT TABLE (Employee assignments)
-- ============================================
INSERT INTO E_ASSIGNMENT (a_id, e_id) VALUES 
(1, 21), (1, 22),   -- Window cleaning team
(2, 23), (2, 24),   -- Floor polishing
(3, 25),            -- Door repair
(4, 26), (4, 27),   -- Leak repair team
(6, 28), (6, 29),   -- HVAC maintenance
(7, 30), (7, 31),   -- Carpet cleaning
(11, 32), (11, 33), -- Exterior painting
(14, 34), (14, 35), -- Pest control
(17, 36), (17, 37), -- Wall repainting
(18, 38), (18, 39), -- Floor waxing
(22, 40), (22, 41), -- Graffiti removal
(24, 42), (24, 43), -- Landscape maintenance
(26, 44), (26, 45), -- Water filter replacement
(28, 46), (28, 47), -- Floor mat cleaning
(29, 48), (29, 49); -- Whiteboard replacement

-- ============================================
-- C_ASSIGNMENT TABLE (Subcontractor assignments)
-- ============================================
INSERT INTO C_ASSIGNMENT (a_id, c_id) VALUES 
(5, 1),   -- Speaker system upgrade
(8, 2),   -- Lighting system retrofit
(9, 3),   -- Elevator modernization
(10, 4),  -- Restroom renovation
(12, 5),  -- Floor tile replacement
(13, 6),  -- Electrical panel upgrade
(15, 7),  -- Fountain pump repair
(16, 8),  -- Gate automation
(19, 9),  -- Window seal replacement
(20, 10), -- Data cabling
(21, 1),  -- Ceiling tile replacement
(23, 2),  -- Fire system inspection
(25, 3),  -- Furniture assembly
(27, 4),  -- Signage installation
(30, 5);  -- Security camera install

-- ============================================
-- ACTIVITY_LOCATIONS TABLE
-- ============================================
INSERT INTO ACTIVITY_LOCATIONS (location_id, a_id) VALUES 
(1, 1),   -- Core A for window cleaning
(31, 2),  -- A101 for floor polishing
(2, 3),   -- Core B for door repair
(48, 4),  -- B103 for leak repair
(30, 5),  -- Jockey Aud for speaker upgrade
(13, 6),  -- Core P for HVAC
(35, 7),  -- A201 for carpet cleaning
(10, 8),  -- Block L for lighting
(11, 9),  -- Block M for elevator
(19, 10), -- Core S Comm for restroom
(2, 11),  -- Core B for painting
(31, 12), -- A101 for tile replacement
(4, 13),  -- Core D for electrical
(1, 14), (2, 14), (3, 14),  -- Multiple buildings for pest control
(38, 15), -- Fountain Sq for pump repair
(33, 16), -- Main Gate for automation
(36, 17), -- A202 for wall painting
(37, 18), -- A203 for floor waxing
(6, 19),  -- Core F for window seals
(47, 20), -- B102 for data cabling
(32, 21), -- A102 for ceiling tiles
(1, 22), (2, 22), (3, 22),  -- Multiple for graffiti removal
(1, 23), (2, 23), (3, 23),  -- Multiple for fire inspection
(35, 24), -- University Sq for landscape
(34, 25), -- A201 for furniture
(1, 26), (2, 26), (3, 26),  -- Multiple for water filters
(33, 27), -- Main Gate for signage
(31, 28), -- A101 for mat cleaning
(32, 29), -- A102 for whiteboards
(33, 30); -- Main Gate for cameras

-- ============================================
-- CHEMICAL_USAGE TABLE
-- ============================================
INSERT INTO CHEMICAL_USAGE (chemical_id, a_id) VALUES 
(10, 1),   -- Windex for window cleaning
(8, 2),    -- Fantastik for floor polishing
(5, 3),    -- WD-40 for door repair
(7, 4),    -- Zep Degreaser for leak repair
(1, 7),    -- Clorox for carpet cleaning
(13, 10),  -- Pine-Sol for restroom renovation
(2, 11),   -- Lysol for exterior painting
(14, 14),  -- Mean Green for pest control
(6, 17),   -- Krud Kutter for wall repainting
(9, 18),   -- 409 for floor waxing
(4, 22),   -- Goo Gone for graffiti removal
(12, 24),  -- Comet for landscape
(3, 26),   -- Simple Green for water filter areas
(11, 28),  -- Tide for mat cleaning
(15, 29);  -- Fabuloso for whiteboard areas

-- ============================================
-- BUILDING_SUPERVISION TABLE (5 buildings)
-- ============================================
INSERT INTO BUILDING_SUPERVISION (building_id, e_id) VALUES 
(1, 2),   -- Core A -> Sarah Wong
(10, 3),  -- Block L -> David Li
(11, 4),  -- Block M -> Jennifer Zhang
(18, 5),  -- Core S -> Kevin Tsang
(22, 6);  -- Block V -> Amy Lau
