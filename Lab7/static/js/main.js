document.addEventListener('DOMContentLoaded', function() {
    
    document.getElementById("enableInputButton").addEventListener("click", function() {

        var studentName = document.getElementById("student_name");
        studentName.disabled = false;
    
        var studentLastName = document.getElementById("student_last_name");
        studentLastName.disabled = false;
    
        var studentAge = document.getElementById("student_age");
        studentAge.disabled = false;
    
        this.style.display = "none";
        
        document.getElementById("submitButton").style.display = "";
        document.getElementById("disableInputButton").style.display = "";
    });
    
    document.getElementById("disableInputButton").addEventListener("click", function() {
    
        var studentName = document.getElementById("student_name");
        studentName.disabled = true;
    
        var studentLastName = document.getElementById("student_last_name");
        studentLastName.disabled = true;
    
        var studentAge = document.getElementById("student_age");
        studentAge.disabled = true;
    
        this.style.display = "none";
        document.getElementById("submitButton").style.display = "none";
    
        document.getElementById("enableInputButton").style.display = "";
    });
});