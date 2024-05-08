import pytest
import os
import webbrowser

# pytest session sonunda çalışacak bir fixture tanımlayın
@pytest.fixture(scope="session", autouse=True)
def report_after_tests(request):
    # Testler bittikten sonra çalışacak kod
    def generate_report():
        # HTML rapor dosyasının adı
        report_file = "report.html"

        # HTML rapor dosyasının tam yolu
        report_path = os.path.abspath(report_file)

        # Check if the report file exists
        if not os.path.exists(report_path):
            print(f"Report file not found: {report_path}")
            return

        # HTML rapor dosyasının URL'si
        report_url = "file://" + report_path

        # URL'yi konsola yazdır
        print("HTML report URL:", report_url)

        # URL'yi varsayılan web tarayıcısında aç
        webbrowser.open(report_url)

    # Testler bittikten sonra generate_report fonksiyonunu çalıştır
    request.addfinalizer(generate_report)