// 휴대폰 번호 입력 부분
function changePhone1(){
  const phone1 = document.getElementById("phone1").value;
  if(phone1.length === 3){
      document.getElementById("phone2").focus();
  }
}

function changePhone2(){
  const phone2 = document.getElementById("phone2").value;
  if(phone2.length === 4){
      document.getElementById("phone3").focus();
  }
}

function changePhone3(){
  const phone3 = document.getElementById("phone3").value;
  if(phone3.length === 4){
      // 포커스 관련 코드 추가 필요
  }
}

// 가입부분 체크
function signUpCheck(){
  let email = document.getElementById("email").value;
  let name = document.getElementById("name").value;
  let password = document.getElementById("password").value;
  let passwordCheck = document.getElementById("passwordCheck").value;
  let area = document.getElementById("area").value;
  let gender_man = document.getElementById("gender_man").checked;
  let gender_woman = document.getElementById("gender_woman").checked;
  let check = true;

  // 이메일 확인
  if(email.includes('@')){
      let emailId = email.split('@')[0];
      let emailServer = email.split('@')[1];
      if(emailId === "" || emailServer === ""){
          document.getElementById("emailError").innerHTML = "이메일이 올바르지 않습니다.";
          check = false;
      } else {
          document.getElementById("emailError").innerHTML = "";
      }
  } else {
      document.getElementById("emailError").innerHTML = "이메일이 올바르지 않습니다.";
      check = false;
  }

  // 이름 확인
  if(name === ""){
      document.getElementById("nameError").innerHTML = "이름이 올바르지 않습니다.";
      check = false;
  } else {
      document.getElementById("nameError").innerHTML = "";
  }

  // 비밀번호 확인
  if(password !== passwordCheck){
      document.getElementById("passwordError").innerHTML = "";
      document.getElementById("passwordCheckError").innerHTML = "비밀번호가 동일하지 않습니다.";
      check = false;
  } else {
      document.getElementById("passwordError").innerHTML = "";
      document.getElementById("passwordCheckError").innerHTML = "";
  }

  if(password === ""){
      document.getElementById("passwordError").innerHTML = "비밀번호를 입력해주세요.";
      check = false;
  }

  if(passwordCheck === ""){
      document.getElementById("passwordCheckError").innerHTML = "비밀번호를 다시 입력해주세요.";
      check = false;
  }

  // 지역선택 확인
  if(area === "지역을 선택하세요."){
      document.getElementById("areaError").innerHTML = "지역을 선택해주세요.";
      check = false;
  } else {
      document.getElementById("areaError").innerHTML = "";
  }

  // 성별 체크 확인
  if(!gender_man && !gender_woman){
      document.getElementById("genderError").innerHTML = "성별을 선택해주세요.";
      check = false;
  } else {
      document.getElementById("genderError").innerHTML = "";
  }

  // 가입 조건을 모두 만족했는지 확인
  if(check){
      document.getElementById("signUpForm").submit(); // HTML 폼 제출
  }
}