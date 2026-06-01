-- KB-1: Schéma PostgreSQL initial minimal pour Cicero

CREATE TABLE cities (
    id BIGSERIAL PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    country_code CHAR(2) NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE monuments (
    id BIGSERIAL PRIMARY KEY,
    city_id BIGINT NOT NULL REFERENCES cities(id) ON DELETE RESTRICT,
    slug TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    year_built INTEGER,
    architect TEXT,
    practical_info JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE media (
    id BIGSERIAL PRIMARY KEY,
    monument_id BIGINT NOT NULL REFERENCES monuments(id) ON DELETE CASCADE,
    media_type TEXT NOT NULL,
    url TEXT NOT NULL,
    title TEXT,
    credit TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE monument_i18n (
    monument_id BIGINT NOT NULL REFERENCES monuments(id) ON DELETE CASCADE,
    lang_code VARCHAR(8) NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    PRIMARY KEY (monument_id, lang_code)
);
