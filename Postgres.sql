CREATE TABLE "User" (
  "id" int PRIMARY KEY,
  "username" varchar(150) UNIQUE,
  "password" varchar(128),
  "email" varchar(254) UNIQUE,
  "phone" varchar(15),
  "profile_image" varchar(255),
  "role" enum(buyer,dealer,admin)
);

CREATE TABLE "Car" (
  "id" int PRIMARY KEY,
  "dealer_id" int,
  "make" varchar(50),
  "model" varchar(50),
  "year" int,
  "color" varchar(20),
  "price" decimal(10,2),
  "mileage" int,
  "fuel_type" enum(petrol,diesel,electric,hybrid),
  "transmission" enum(manual,automatic),
  "condition" enum(new,used),
  "description" text,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "CarImage" (
  "id" int PRIMARY KEY,
  "car_id" int,
  "image" varchar(255),
  "image_type" enum(front,side,back,interior)
);

CREATE TABLE "Wishlist" (
  "id" int PRIMARY KEY,
  "user_id" int,
  "car_id" int,
  "created_at" datetime
);

CREATE TABLE "CarComparison" (
  "id" int PRIMARY KEY,
  "user_id" int,
  "car1_id" int,
  "car2_id" int,
  "created_at" datetime
);

CREATE TABLE "Review" (
  "id" int PRIMARY KEY,
  "user_id" int,
  "car_id" int,
  "rating" int,
  "comment" text,
  "created_at" datetime
);

CREATE TABLE "Message" (
  "id" int PRIMARY KEY,
  "sender_id" int,
  "receiver_id" int,
  "car_id" int,
  "content" text,
  "timestamp" datetime
);

CREATE TABLE "SearchHistory" (
  "id" int PRIMARY KEY,
  "user_id" int,
  "search_query" varchar(255),
  "created_at" datetime
);

CREATE TABLE "Transaction" (
  "id" int PRIMARY KEY,
  "buyer_id" int,
  "car_id" int,
  "amount" decimal(10,2),
  "status" enum(pending,completed,failed),
  "created_at" datetime
);

CREATE TABLE "Advertisement" (
  "id" int PRIMARY KEY,
  "car_id" int,
  "dealer_id" int,
  "is_featured" boolean,
  "start_date" date,
  "end_date" date,
  "price" decimal(10,2)
);

ALTER TABLE "Car" ADD FOREIGN KEY ("dealer_id") REFERENCES "User" ("id");

ALTER TABLE "CarImage" ADD FOREIGN KEY ("car_id") REFERENCES "Car" ("id");

ALTER TABLE "Wishlist" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "Wishlist" ADD FOREIGN KEY ("car_id") REFERENCES "Car" ("id");

ALTER TABLE "CarComparison" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "CarComparison" ADD FOREIGN KEY ("car1_id") REFERENCES "Car" ("id");

ALTER TABLE "CarComparison" ADD FOREIGN KEY ("car2_id") REFERENCES "Car" ("id");

ALTER TABLE "Review" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "Review" ADD FOREIGN KEY ("car_id") REFERENCES "Car" ("id");

ALTER TABLE "Message" ADD FOREIGN KEY ("sender_id") REFERENCES "User" ("id");

ALTER TABLE "Message" ADD FOREIGN KEY ("receiver_id") REFERENCES "User" ("id");

ALTER TABLE "Message" ADD FOREIGN KEY ("car_id") REFERENCES "Car" ("id");

ALTER TABLE "SearchHistory" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "Transaction" ADD FOREIGN KEY ("buyer_id") REFERENCES "User" ("id");

ALTER TABLE "Transaction" ADD FOREIGN KEY ("car_id") REFERENCES "Car" ("id");

ALTER TABLE "Advertisement" ADD FOREIGN KEY ("car_id") REFERENCES "Car" ("id");

ALTER TABLE "Advertisement" ADD FOREIGN KEY ("dealer_id") REFERENCES "User" ("id");
