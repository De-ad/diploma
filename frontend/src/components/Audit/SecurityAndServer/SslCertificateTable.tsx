import { SslCertificate } from "../../../constants/types";
import styles from "./styles.module.css";

type Props = {
  certificate: SslCertificate;
  title: string;
};
export const SslCertificateTable = ({ certificate, title }: Props) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const datePart = date.toISOString().split("T")[0];
    const timePart = date.toISOString().split("T")[1].split(".")[0];
    return `${datePart} ${timePart}`;
  };
  return (
    <table className={styles.table}>
      <thead>
        <tr>
          <th>{title}</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Тема</td>
          <td>{certificate.subject}</td>
        </tr>
        <tr>
          <td>Издатель</td>
          <td>{certificate.issuer}</td>
        </tr>
        <tr>
          <td>Срок действия с</td>
          <td>{formatDate(certificate.notValidBefore)}</td>
        </tr>
        <tr>
          <td>Срок действия до</td>
          <td>{formatDate(certificate.notValidAfter)}</td>
        </tr>
        <tr>
          <td>Алгоритм подписи</td>
          <td>{certificate.signatureAlgorithm}</td>
        </tr>
        <tr>
          <td>Версия</td>
          <td>{certificate.version}</td>
        </tr>
      </tbody>
    </table>
  );
};
