-- Blog Platform Schema Design (T2 example)
-- Entities: User, Post, Comment, Tag, PostTag

-- Users table with authentication fields
CREATE TABLE users (
  user_id BIGSERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Posts table with soft delete
CREATE TABLE posts (
  post_id BIGSERIAL PRIMARY KEY,
  author_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  content TEXT NOT NULL,
  published_at TIMESTAMPTZ,
  deleted_at TIMESTAMPTZ,  -- Soft delete
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Comments with nested threading support
CREATE TABLE comments (
  comment_id BIGSERIAL PRIMARY KEY,
  post_id BIGINT NOT NULL REFERENCES posts(post_id) ON DELETE CASCADE,
  author_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  parent_comment_id BIGINT REFERENCES comments(comment_id) ON DELETE CASCADE,
  content TEXT NOT NULL CHECK (LENGTH(content) <= 1000),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tags for categorization (many-to-many)
CREATE TABLE tags (
  tag_id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
  post_id BIGINT REFERENCES posts(post_id) ON DELETE CASCADE,
  tag_id INTEGER REFERENCES tags(tag_id) ON DELETE CASCADE,
  PRIMARY KEY (post_id, tag_id)
);

-- Indexes for common query patterns
CREATE INDEX idx_posts_author ON posts(author_id, created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_posts_published ON posts(published_at DESC) WHERE published_at IS NOT NULL AND deleted_at IS NULL;
CREATE INDEX idx_comments_post ON comments(post_id, created_at);
CREATE INDEX idx_tags_name ON tags(name);
