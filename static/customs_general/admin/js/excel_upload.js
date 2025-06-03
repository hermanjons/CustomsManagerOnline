
document.addEventListener("DOMContentLoaded", function() {
    let modal = document.getElementById("excelUploadModal");
    let excel_modal_btn = document.getElementById("openExcelModal");
    let excel_modal_cls_spn = document.getElementsByClassName("close")[0];
    let form = document.getElementById("excelUploadForm");
    let messageDiv = document.getElementById("uploadMessage");
    let progressContainer = document.getElementById("progressContainer");
    let progressBar = document.getElementById("progressBar");
    const uploadMessage = document.getElementById("uploadMessage");
    const uploadSuccess = document.getElementById("uploadSuccess");
    const successMessageText = document.getElementById("successMessageText");
    const uploadError = document.getElementById("uploadError");
    const errorMessageText = document.getElementById("errorMessageText");
    const uploadFailedRows = document.getElementById("uploadFailedRows");
    const failedRowCountText = document.getElementById("failedRowCountText");
    const failedDownloadLink = document.getElementById("failedDownloadLink");




    excel_modal_btn.onclick = function() {
        modal.style.display = "block";


    };

    excel_modal_cls_spn.onclick = function() {
        modal.style.display = "none";
        messageDiv.innerHTML = "";
    };

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
            messageDiv.innerHTML = "";

        }
    };



function pollRealProgress() {
    fetch(config.uploadProgressUrl)
        .then(res => res.json())
        .then(data => {
            let progress = data.progress || 0;
            progressBar.style.width = progress + "%";
            progressBar.innerText = progress + "%";

            if (progress < 100) {
                setTimeout(pollRealProgress, 500);
            }
        })
        .catch(error => {
            console.error("⛔ Progress error:", error);
        });
}




function resetProgress() {
        progressBar.style.width = "0%";
        progressBar.innerText = "0%";
    }

form.onsubmit = function (event) {
  event.preventDefault();

  const formData = new FormData(form);

  // Mesaj kutularını sıfırla
  uploadSuccess.classList.add("hidden");
  uploadError.classList.add("hidden");
  uploadFailedRows.classList.add("hidden");
  uploadMessage.classList.remove("hidden");

  // Progress çubuğu sıfırla + göster
  progressContainer.style.display = "block";
  resetProgress();
  pollRealProgress();

  fetch(config.uploadExcelUrl, {
    method: "POST",
    body: formData,
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        // ✅ Başarılı mesajı göster
        successMessageText.innerText = data.message;
        uploadSuccess.classList.remove("hidden");

        if (data.failed_rows_count > 0) {
          // ⚠️ Hatalı satırlar varsa göster
          failedRowCountText.innerText = data.failed_rows_count;
          failedDownloadLink.href = data.failed_rows_download_url;
          uploadFailedRows.classList.remove("hidden");
        }
      } else {
        // ❌ Hata mesajı göster
        errorMessageText.innerText = data.error;
        uploadError.classList.remove("hidden");
      }
    })
    .catch(error => {
      // ⛔ İstek sırasında teknik hata olursa
      errorMessageText.innerText = "Bir hata oluştu!";
      uploadError.classList.remove("hidden");
    });
};

});
