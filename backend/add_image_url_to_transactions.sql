-- Add image_url column to transactions table if it doesn't exist
ALTER TABLE transactions ADD COLUMN image_url TEXT;

-- Update existing rows to have NULL for image_url (or a default value if needed)
-- UPDATE transactions SET image_url = NULL WHERE image_url IS NULL;
