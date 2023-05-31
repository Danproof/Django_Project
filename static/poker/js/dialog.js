;(function () {
    const modal = new bootstrap.Modal(document.getElementById("modal"))
  
    htmx.on("htmx:afterSwap", (e) => {
      // Response targeting #dialog => show the modal
      if (e.detail.target.id == "dialog") {
        if (e.detail.xhr.responseURL.includes("table")) {
          const responseURL = e.detail.xhr.responseURL;
          const segments = responseURL.split("/")
          const table = segments[segments.length - 2];
          location.href = table;
        }
        modal.show()
      }

    })
  
    htmx.on("htmx:beforeSwap", (e) => {
      // Empty response targeting #dialog => hide the modal
      if ((e.detail.target.id == "dialog") && !e.detail.xhr.response) {
        modal.hide()
        location.reload()
      }
    })
  
    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
      document.getElementById("dialog").innerHTML = ""
    })
})()
