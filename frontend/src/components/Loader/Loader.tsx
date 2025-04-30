import { HashLoader } from "react-spinners";
import styles from "./styles.module.css";

export const Loader = () => {
  // add long loading message
  return (
    <div className={styles.loading}>
      <HashLoader color="#8c61ff" />
    </div>
  );
};
