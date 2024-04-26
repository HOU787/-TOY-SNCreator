document.querySelectorAll(".col").forEach((col) => {
  col.addEventListener("click", function (event) {
    const loggedIn = this.getAttribute("data-logged-in") === "true";
    if (!loggedIn) {
      alert("Please log in to access this feature.");
    } else {
      const genre = this.getAttribute("data-genre");
      document.getElementById("genreInput").value = genre;
      document.getElementById("genreName").innerHTML = genre;
    }
  });
});

function showLoginModal() {
  $("#loginModal").modal("show");
}

$(document).ready(function () {
  // 로그인 모달 표시
  $("#log-in").click(function () {
    $("#loginModal").modal("show");
  });

  // 회원가입 링크 클릭 시
  $("#signupLink").click(function () {
    $("#loginModal").modal("hide"); // 로그인 모달 닫기
    $("#signUpModal").modal("show"); // 회원가입 모달 열기
  });

  // 회원가입 버튼 클릭 시 회원가입 모달 표시
  $("#sign-up").click(function () {
    $("#signUpModal").modal("show");
  });
});

// 회원가입 처리
document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("signinForm")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // 기본 제출 이벤트 방지

      var formData = new FormData(event.target);
      var object = {};
      formData.forEach((value, key) => {
        object[key] = value;
      });

      var json = JSON.stringify(object);

      fetch("/signin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          userId: document.getElementById("newUserId").value,
          password: document.getElementById("newPassword").value,
          nickname: document.getElementById("newNickname").value,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);

          // success 일 때만 modal hide
          if (data.result === "success") {
            $("#signUpModal").modal("hide");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("An error occurred. Please try again.");
        });
    });
});

// login
document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");

  loginForm.addEventListener("submit", function (event) {
    event.preventDefault(); // 기본 폼 제출 이벤트 방지

    const userId = document.getElementById("userId").value;
    const password = document.getElementById("password").value;

    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userId: userId,
        password: password,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message); // 서버 응답 메시지를 alert로 표시
        if (data.result === "success") {
          $("#loginModal").modal("hide");
          location.reload(true);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred. Please try again later.");
      });
  });
});

// log-out
document.getElementById("log-out").addEventListener("click", function () {
  fetch("/logout");
  alert("Logout successful!");
  location.reload(true);
});

document
  .getElementById("nameForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    let formData = new FormData(this);

    // 스피너를 표시
    console.log("Showing spinner");
    document.getElementById("spinner").style.display = "block";
    document.getElementById("storyText").style.display = "none";

    fetch("/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Hiding spinner");
        document.getElementById("spinner").style.display = "none";
        document.getElementById("storyText").style.display = "block";
        document.getElementById("storyText").value = data.text;
        document.getElementById("modalTitle").textContent = `${formData.get(
          "nickname"
        )}'s ${formData.get("genre")} Story`;

        var confirmationModal = new bootstrap.Modal(
          document.getElementById("confirmationModal")
        );
        confirmationModal.show();
        $("#nameModal").modal("hide");
      })
      .catch((error) => {
        console.error("Error:", error);
        document.getElementById("spinner").style.display = "none";
        alert("An error occurred while fetching the story. Please try again.");
      });
  });

function saveStory() {
  var storyText = document.getElementById("storyText").value; // textarea에서 텍스트를 가져옵니다.
  var form = new FormData();
  form.append("text", storyText);

  fetch("/download", {
    method: "POST",
    body: form,
  })
    .then((response) => response.blob())
    .then((blob) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = "Your_Story.pdf";
      document.body.appendChild(a); // 링크 요소를 문서에 추가
      a.click(); // 프로그래밍 방식으로 클릭 이벤트를 발생시킵니다.
      a.remove(); // 다운로드 후 링크 요소 제거
      window.URL.revokeObjectURL(url); // 생성된 URL 해제
    })
    .catch((error) => console.error("Error downloading the file:", error));
}
