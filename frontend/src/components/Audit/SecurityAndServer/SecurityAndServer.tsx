import { Security } from "../../../constants/types";
import { SECURITY_AND_SERVER_PARAMS } from "../../../constants/text";
import { Card } from "../Base/Card";
import styles from "./styles.module.css";
import { SslCertificateTable } from "./SslCertificateTable";
import { MdCheck, MdClose } from "react-icons/md";

type Props = {
  security: Security;
};
export const SecurityAndServer = ({ security }: Props) => {
  const getCardProps = (param: (typeof SECURITY_AND_SERVER_PARAMS)[number]) => {
    let result = true;
    let location: string[] = [];

    switch (param.key) {
      case "spfRecord":
        result = security.spfRecord.found;
        break;

      case "unsafeLinks":
        location = security.allUnsafeLinks;
        result = security.allUnsafeLinks.length < 0;
        break;
      case "http2Support":
        result = security.http2Support;
        break;
      default:
        break;
    }

    return {
      title: param.title,
      result,
      resultText: result ? param.positiveResultText : param.negativeResultText,
      description: param.description,
      location,
    };
  };

  return (
    <div className={styles.block}>
      <div>
        {SECURITY_AND_SERVER_PARAMS.map((param) => (
          <Card key={param.key} {...getCardProps(param)} />
        ))}
      </div>

      <div className={styles.sslBlock}>
        <h2>SSL и HTTPS </h2>

        <div>
          <p>
            {security.sslCertificates.checks.hostnameMatches ? (
              <>
                <MdCheck className={styles.iconSuccess} /> Имя хоста правильно
                указано в сертификате
              </>
            ) : (
              <>
                <MdClose className={styles.iconError} /> Имя хоста неправильно
                указано в сертификате
              </>
            )}
          </p>
          <p>
            {security.sslCertificates.checks.notExpired ? (
              <>
                <MdCheck className={styles.iconSuccess} /> Срок действия
                сертификата не истек
              </>
            ) : (
              <>
                <MdClose className={styles.iconError} /> Срок действия
                сертификата истек
              </>
            )}
          </p>
          <p>
            {security.sslCertificates.checks.notUsedBeforeActivationDate ? (
              <>
                <MdCheck className={styles.iconSuccess} /> Сертификат не
                используется до даты активации
              </>
            ) : (
              <>
                <MdClose className={styles.iconError} /> Сертификат используется
                до даты активации
              </>
            )}
          </p>
          <p>
            {security.sslCertificates.checks.trustedByMajorBrowsers ? (
              <>
                <MdCheck className={styles.iconSuccess} /> Сертификат одобрен
                большинством браузеров
              </>
            ) : (
              <>
                <MdClose className={styles.iconError} /> Сертификат не одобрен
                большинством браузеров
              </>
            )}
          </p>
          <p>
            {security.sslCertificates.checks.usesSecureHash ? (
              <>
                <MdCheck className={styles.iconSuccess} /> Сертификат был
                подписан с использованием безопасной хеш-функции
              </>
            ) : (
              <>
                <MdClose className={styles.iconError} /> Сертификат не был
                подписан с использованием безопасной хеш-функции
              </>
            )}
          </p>
        </div>
        <div className={styles.tableWrapper}>
          <SslCertificateTable
            certificate={security.sslCertificates.serverCertificate}
            title={"Серверный сертификат"}
          />
          <SslCertificateTable
            certificate={security.sslCertificates.rootCertificate}
            title={`Корневой\u00A0сертификат`}
          />
        </div>
      </div>
    </div>
  );
};
