CREATE TABLE IF NOT EXISTS publication_queue (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),

  campaign_id uuid REFERENCES campaigns(id) ON DELETE SET NULL,

  channel text NOT NULL,
  -- instagram, facebook, tiktok, google_business, whatsapp

  content_type text NOT NULL,
  -- carousel, single_image, reel_script, text_post, story, google_post

  title text,
  caption text,
  cta text,
  keyword text,

  media_payload jsonb,
  -- imagens, slides, links, arquivos, instruções de arte

  post_payload jsonb,
  -- payload final enviado para API do canal

  status text NOT NULL DEFAULT 'queued',
  -- queued, publishing, published, failed, blocked, skipped, deleted_manually

  scheduled_for timestamptz,
  published_at timestamptz,

  attempts integer DEFAULT 0,
  last_error text,

  channel_post_id text,
  post_url text,

  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);
