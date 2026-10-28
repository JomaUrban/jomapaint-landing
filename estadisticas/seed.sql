-- Webs del grupo. IDs fijos: son los data-website-id que va en cada web.
-- Idempotente: se ejecuta en cada despliegue y no toca lo que ya existe.
INSERT INTO website (website_id, name, domain, user_id, created_by)
SELECT v.id::uuid, v.name, v.domain, u.user_id, u.user_id
FROM (VALUES
  ('a3a6b5ee-66b7-4893-a295-2e6e9fe188b4', 'JomaPaint',  'paint.joma.es'),
  ('72937a60-e911-4d1e-bf34-4e358686f870', 'Joma Urban', 'jomaurban.com'),
  ('7d999b89-c4ff-4e67-83cc-b6f5cd541703', 'Normo',      'normo.es'),
  ('86cc56b6-fb47-4115-87a9-3eda024bf97d', 'Joma',       'joma.es'),
  ('1272970f-f4e1-4967-9c29-0de23b16aee3', 'Joma Urban (staging)', 'staging.jomaurban.com'),
  ('f9227910-44f9-4cc7-9834-24ef6ec1fb9b', 'Ekilabs',    'ekilabs.com'),
  ('4f420787-9477-4bcc-a5d2-08beb430530f', 'Buzonia',    'buzonia.com'),
  ('d27dbbce-5e95-4968-b8ec-254fb596cd68', 'Buzones Costasol', 'buzonescostasol.com'),
  ('a4b8062f-1394-4c5e-b19b-093ceac38c9e', 'Cortelaser', 'paint.joma.es')
) AS v(id, name, domain)
CROSS JOIN (SELECT user_id FROM "user" WHERE username = 'admin' AND deleted_at IS NULL LIMIT 1) u
ON CONFLICT (website_id) DO NOTHING;
