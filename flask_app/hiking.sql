-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema hiking_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `hiking_schema` ;

-- -----------------------------------------------------
-- Schema hiking_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `hiking_schema` DEFAULT CHARACTER SET utf8 ;
USE `hiking_schema` ;

-- -----------------------------------------------------
-- Table `hiking_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiking_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `confirm_password` VARCHAR(255) NULL,
  `experience` VARCHAR(255) NULL,
  `about_me` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hiking_schema`.`hikes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiking_schema`.`hikes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `description` VARCHAR(255) NULL,
  `city` VARCHAR(255) NULL,
  `state` VARCHAR(255) NULL,
  `difficulty` VARCHAR(255) NULL,
  `likes` INT NULL DEFAULT 0,
  `dislikes` INT NULL DEFAULT 0,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_hikes_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_hikes_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `hiking_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hiking_schema`.`favorites`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiking_schema`.`favorites` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  `hike_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_favorites_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_favorites_hikes1_idx` (`hike_id` ASC) VISIBLE,
  CONSTRAINT `fk_favorites_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `hiking_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_favorites_hikes1`
    FOREIGN KEY (`hike_id`)
    REFERENCES `hiking_schema`.`hikes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hiking_schema`.`comments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiking_schema`.`comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `message` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  `hike_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comments_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_comments_hikes1_idx` (`hike_id` ASC) VISIBLE,
  CONSTRAINT `fk_comments_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `hiking_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comments_hikes1`
    FOREIGN KEY (`hike_id`)
    REFERENCES `hiking_schema`.`hikes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
