document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".title").forEach(function (element) {
    element.addEventListener("click", function () {
      const postId = this.getAttribute("data-postid"); // 제목 클릭 시 해당 postId 추출
      fetchStory(postId); // fetchStory 함수 호출, postId를 인자로 전달
    });
  });
});

function fetchStory(postId) {
  $.ajax({
    url: "/get-post",
    type: "GET",
    data: { postId: postId },
    success: function (data) {
      $("#titleText").val(data.title);
      $("#storyText").text(data.text);
      $("#modalTitle").val(data.genre);
      $("#modalTitle").text(data.cheracter + "'s " + data.genre + " Story");
      $("#confirmationModal").modal("show");
    },
    error: function () {
      alert("Error: Could not retrieve story.");
    },
  });
}
