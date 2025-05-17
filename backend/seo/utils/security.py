import socket
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime
from models.analysis import Check, ErrorResult
from cryptography.x509.oid import ExtensionOID, NameOID
import subprocess

# should have clean url like example.com
# TODO: check not home page
import asyncio


async def check_ssl_certificate(url: str):
    clean_url = url.replace("http://", "").replace("https://", "").rstrip("/")
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=clean_url) as s:
            s.connect((clean_url, 443))

        return Check(
            found=True,
            status_code=200,
            message="Has valid ssl certificate",
            file_extension=None,
        )

    except Exception as e:
        return ErrorResult(error="Has invalid ssl certificate, error: " + str(e))


def fetch_full_cert_chain_openssl(
    hostname: str, port: int = 443
) -> list[x509.Certificate]:
    """
    Uses subprocess to call openssl and extract the full certificate chain in PEM format.
    """
    try:
        result = subprocess.run(
            [
                "openssl",
                "s_client",
                "-connect",
                f"{hostname}:{port}",
                "-showcerts",
                "-servername",
                hostname,
            ],
            input="Q\n",
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=10,
        )
        output = result.stdout

        # Extract PEM certificates
        certs = []
        pem_blocks = output.split("-----BEGIN CERTIFICATE-----")
        for pem in pem_blocks[1:]:
            full_pem = (
                "-----BEGIN CERTIFICATE-----"
                + pem.split("-----END CERTIFICATE-----")[0]
                + "-----END CERTIFICATE-----"
            )
            cert = x509.load_pem_x509_certificate(full_pem.encode(), default_backend())
            certs.append(cert)
        return certs
    except Exception as e:
        print(f"Error fetching certificate chain: {e}")
        return []


def get_formatted_certificate_chain(hostname: str, port: int = 443):
    cert_chain = fetch_full_cert_chain_openssl(hostname, port)

    formatted = {
        "server_certificate": {},
        "intermediate_certificates": [],
        "root_certificate": {},
    }

    if not cert_chain:
        return formatted

    total = len(cert_chain)

    for idx, cert in enumerate(cert_chain):
        cert_info = {
            "subject": cert.subject.rfc4514_string(),
            "issuer": cert.issuer.rfc4514_string(),
            "not_valid_before": cert.not_valid_before.isoformat(),
            "not_valid_after": cert.not_valid_after.isoformat(),
            "signature_algorithm": cert.signature_hash_algorithm.name,
            "version": cert.version.name,
        }

        if idx == 0:
            formatted["server_certificate"] = cert_info
        elif idx < total - 1:
            formatted["intermediate_certificates"].append(cert_info)
        else:
            formatted["root_certificate"] = cert_info

    return formatted


def get_ssl_checks(hostname: str, port: int = 443):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
    conn.connect((hostname, port))
    der_cert = conn.getpeercert(binary_form=True)
    conn.close()

    server_cert = x509.load_der_x509_certificate(der_cert, default_backend())
    now = datetime.utcnow()
    not_used_before = now >= server_cert.not_valid_before
    not_expired = now <= server_cert.not_valid_after

    try:
        sans = server_cert.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        ).value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        sans = []

    try:
        cn = server_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    except IndexError:
        cn = ""

    hostname_valid = hostname in sans or hostname == cn

    try:
        pyssl_context = ssl.create_default_context()
        pyssl_context.check_hostname = True
        with pyssl_context.wrap_socket(
            socket.create_connection((hostname, port)), server_hostname=hostname
        ):
            trusted_by_browsers = True
    except Exception:
        trusted_by_browsers = False

    secure_hash = server_cert.signature_hash_algorithm.name.lower() not in [
        "md5",
        "sha1",
    ]

    return {
        "checks": {
            "not_used_before_activation_date": not_used_before,
            "not_expired": not_expired,
            "hostname_matches": hostname_valid,
            "trusted_by_major_browsers": trusted_by_browsers,
            "uses_secure_hash": secure_hash,
        }
    }


async def get_formatted_certificate_chain_async(hostname: str, port: int = 443):
    return await asyncio.to_thread(get_formatted_certificate_chain, hostname, port)


async def get_ssl_checks_async(hostname: str, port: int = 443):
    return await asyncio.to_thread(get_ssl_checks, hostname, port)
