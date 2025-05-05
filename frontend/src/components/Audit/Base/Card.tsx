import React, { useState } from "react";
import { MdCheck, MdClose, MdExpandMore, MdExpandLess } from "react-icons/md";
import styles from "./styles.module.css";

type SeoCardProps = {
  title: string;
  result: boolean;
  resultText: string;
  description?: string;
  location?: string[];
};

export const Card = ({
  title,
  result,
  resultText,
  description,
  location,
}: SeoCardProps) => {
  const [open, setOpen] = useState(false);

  return (
    <div className={styles.card}>
      <div className={styles.header} onClick={() => setOpen(!open)}>
        <div className={styles.titleSection}>
          {result ? (
            <MdCheck className={styles.iconSuccess} />
          ) : (
            <MdClose className={styles.iconError} />
          )}
          <h3 className={styles.title}>{title}</h3>
        </div>
        <div className={styles.rightSection}>
          <p className={styles.message}>{resultText}</p>
          {open ? <MdExpandLess /> : <MdExpandMore />}
        </div>
      </div>
      {open && (
        <div className={styles.description}>
          {description && <p>{description}</p>}
          {location?.length > 0 && (
            <div className={styles.location}>
              <strong>Обнаружено на:</strong>
              {location.map((link, index) => (
                <p key={index}>
                  {link.startsWith("http") || link.startsWith("mailto:") ? (
                    <a
                      href={link.split(" ")[0]}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {link}
                    </a>
                  ) : (
                    <span>{link}</span>
                  )}
                </p>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
