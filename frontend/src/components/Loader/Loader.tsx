import styles from "./styles.module.css";

export const Loader = () => {
  return (
    <div className={styles.loading}>
      <p>Загрузка...</p>
    </div>
  );
};
