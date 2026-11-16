CREATE UNIQUE INDEX match_active_f ON topic_matches(qbank_report,flashcards_report,flashcards_ordinal) WHERE active=1;

CREATE UNIQUE INDEX match_active_q ON topic_matches(qbank_report,flashcards_report,qbank_ordinal) WHERE active=1;

CREATE UNIQUE INDEX planner_active_topic ON planner_items(topic_key)
                    WHERE status IN ('sugerido','aguardando_validacao','aprovado_usuario','aplicado_manualmente');

CREATE INDEX records_topic ON records(topic_id);

CREATE INDEX reports_content ON reports(content_sha256);

CREATE TABLE algorithm_parameters(version INTEGER PRIMARY KEY,payload TEXT NOT NULL,created_at TEXT NOT NULL);

CREATE TABLE algorithm_selections(id INTEGER PRIMARY KEY,parameter_version INTEGER NOT NULL REFERENCES algorithm_parameters(version),created_at TEXT NOT NULL);

CREATE TABLE assessment_contexts (
                    row_id TEXT PRIMARY KEY, qbank_report TEXT NOT NULL REFERENCES reports(file_sha256),
                    flashcards_report TEXT NOT NULL REFERENCES reports(file_sha256),
                    qbank_ordinal INTEGER, flashcards_ordinal INTEGER,
                    path TEXT NOT NULL, revision INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY(qbank_report,qbank_ordinal) REFERENCES records(report_id,ordinal),
                    FOREIGN KEY(flashcards_report,flashcards_ordinal) REFERENCES records(report_id,ordinal)
                );

CREATE TABLE audit_events (
                    id INTEGER PRIMARY KEY, created_at TEXT NOT NULL, event TEXT NOT NULL,
                    report_id TEXT NOT NULL REFERENCES reports(file_sha256), details TEXT NOT NULL
                );

CREATE TABLE classifier_policies (
                    id INTEGER PRIMARY KEY, name TEXT NOT NULL, payload TEXT NOT NULL,
                    digest TEXT UNIQUE NOT NULL, created_at TEXT NOT NULL
                );

CREATE TABLE exam_targets (
        id INTEGER PRIMARY KEY,target_id TEXT NOT NULL,version INTEGER NOT NULL,
        action TEXT NOT NULL CHECK(action IN ('save','void')),payload TEXT NOT NULL,
        created_at TEXT NOT NULL,UNIQUE(target_id,version));

CREATE TABLE guide_days (id INTEGER PRIMARY KEY, day TEXT NOT NULL, payload TEXT NOT NULL, digest TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL);

CREATE TABLE guide_settings (id INTEGER PRIMARY KEY, payload TEXT NOT NULL, created_at TEXT NOT NULL);

CREATE TABLE incidence_datasets (id INTEGER PRIMARY KEY, payload TEXT NOT NULL, digest TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL);

CREATE TABLE matching_events (
                    id INTEGER PRIMARY KEY,
                    decision_id INTEGER NOT NULL REFERENCES topic_matches(id),
                    created_at TEXT NOT NULL, action TEXT NOT NULL CHECK(action IN ('aprovar','remover')),
                    details TEXT NOT NULL
                );

CREATE TABLE mock_exam_areas (
        id INTEGER PRIMARY KEY,mock_exam_id INTEGER NOT NULL REFERENCES mock_exams(id),
        area TEXT NOT NULL,questions INTEGER NOT NULL,correct INTEGER NOT NULL);

CREATE TABLE mock_exam_topics (
        id INTEGER PRIMARY KEY,mock_exam_id INTEGER NOT NULL REFERENCES mock_exams(id),
        path TEXT NOT NULL,questions INTEGER NOT NULL,correct INTEGER NOT NULL);

CREATE TABLE mock_exams (
        id INTEGER PRIMARY KEY,exam_key TEXT NOT NULL,version INTEGER NOT NULL,
        action TEXT NOT NULL CHECK(action IN ('save','void')),payload TEXT NOT NULL,
        created_at TEXT NOT NULL,UNIQUE(exam_key,version));

CREATE TABLE observation_events (
                    id INTEGER PRIMARY KEY, observation_id INTEGER NOT NULL REFERENCES observations(id),
                    action TEXT NOT NULL CHECK(action IN ('registrar','desconsiderar')),
                    created_at TEXT NOT NULL, details TEXT NOT NULL
                );

CREATE TABLE observations (
                    id INTEGER PRIMARY KEY, row_id TEXT NOT NULL REFERENCES assessment_contexts(row_id),
                    observation_date TEXT NOT NULL, payload TEXT NOT NULL, digest TEXT NOT NULL,
                    created_at TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)),
                    UNIQUE(row_id,digest)
                );

CREATE TABLE planner_batches (
                    id INTEGER PRIMARY KEY, name TEXT NOT NULL, note TEXT NOT NULL,
                    qbank_report_id TEXT NOT NULL REFERENCES reports(file_sha256),
                    flashcards_report_id TEXT NOT NULL REFERENCES reports(file_sha256),
                    analysis_date TEXT NOT NULL, config TEXT NOT NULL, created_at TEXT NOT NULL
                );

CREATE TABLE planner_events (
                    id INTEGER PRIMARY KEY, item_id INTEGER NOT NULL REFERENCES planner_items(id),
                    action TEXT NOT NULL, previous_status TEXT, new_status TEXT NOT NULL,
                    action_date TEXT NOT NULL, created_at TEXT NOT NULL, details TEXT NOT NULL
                );

CREATE TABLE planner_items (
                    id INTEGER PRIMARY KEY, batch_id INTEGER NOT NULL REFERENCES planner_batches(id),
                    row_id TEXT NOT NULL, topic_key TEXT NOT NULL, snapshot TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('sugerido','aguardando_validacao','aprovado_usuario','aplicado_manualmente','reativado','cancelado')),
                    revision INTEGER NOT NULL DEFAULT 1, note TEXT NOT NULL,
                    reevaluation_date TEXT, approved_date TEXT, applied_date TEXT, reactivated_date TEXT,
                    action_date TEXT NOT NULL, updated_at TEXT NOT NULL, UNIQUE(batch_id,row_id)
                );

CREATE TABLE planning_measurements (
                    id INTEGER PRIMARY KEY, payload TEXT NOT NULL, digest TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL
                );

CREATE TABLE records (
                    report_id TEXT NOT NULL REFERENCES reports(file_sha256),
                    ordinal INTEGER NOT NULL, topic_id TEXT NOT NULL, payload TEXT NOT NULL,
                    PRIMARY KEY (report_id, ordinal)
                );

CREATE TABLE reduction_actions (id INTEGER PRIMARY KEY, payload TEXT NOT NULL, digest TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL);

CREATE TABLE reports (
                    file_sha256 TEXT PRIMARY KEY, content_sha256 TEXT NOT NULL,
                    filename TEXT NOT NULL, kind TEXT NOT NULL, scope TEXT NOT NULL,
                    report_date TEXT, imported_at TEXT NOT NULL,
                    duplicate_of TEXT REFERENCES reports(file_sha256),
                    complete INTEGER NOT NULL, payload TEXT NOT NULL
                );

CREATE TABLE routine_profiles (
                    id INTEGER PRIMARY KEY, name TEXT NOT NULL, payload TEXT NOT NULL, digest TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL
                );

CREATE TABLE study_days (day TEXT PRIMARY KEY,revision INTEGER NOT NULL,payload TEXT NOT NULL,updated_at TEXT NOT NULL);

CREATE TABLE study_errors (
        id INTEGER PRIMARY KEY,error_key TEXT NOT NULL,version INTEGER NOT NULL,
        action TEXT NOT NULL CHECK(action IN ('save','void','resolve')),
        topic_path TEXT NOT NULL,day TEXT NOT NULL,source_session_id TEXT,
        cause TEXT NOT NULL,note TEXT NOT NULL,critical INTEGER NOT NULL CHECK(critical IN (0,1)),
        flashcard_hint TEXT,created_at TEXT NOT NULL,UNIQUE(error_key,version));

CREATE TABLE study_events (id INTEGER PRIMARY KEY,session_id TEXT NOT NULL,version INTEGER NOT NULL,action TEXT NOT NULL,payload TEXT NOT NULL,created_at TEXT NOT NULL,UNIQUE(session_id,version));

CREATE TABLE study_plan_runs (id INTEGER PRIMARY KEY,payload TEXT NOT NULL,digest TEXT NOT NULL UNIQUE,created_at TEXT NOT NULL);

CREATE TABLE study_profiles (id INTEGER PRIMARY KEY,payload TEXT NOT NULL,created_at TEXT NOT NULL);

CREATE TABLE topic_matches (
                    id INTEGER PRIMARY KEY,
                    qbank_report TEXT NOT NULL, flashcards_report TEXT NOT NULL,
                    qbank_ordinal INTEGER NOT NULL, flashcards_ordinal INTEGER NOT NULL,
                    note TEXT NOT NULL CHECK(length(trim(note)) > 0),
                    created_at TEXT NOT NULL,
                    active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)),
                    FOREIGN KEY (qbank_report,qbank_ordinal) REFERENCES records(report_id,ordinal),
                    FOREIGN KEY (flashcards_report,flashcards_ordinal) REFERENCES records(report_id,ordinal)
                );

CREATE TABLE weekly_reviews(id INTEGER PRIMARY KEY,week_key TEXT NOT NULL,version INTEGER NOT NULL,action TEXT NOT NULL CHECK(action IN ('save','void')),payload TEXT NOT NULL,created_at TEXT NOT NULL,UNIQUE(week_key,version));