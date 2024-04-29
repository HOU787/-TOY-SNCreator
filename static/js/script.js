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
