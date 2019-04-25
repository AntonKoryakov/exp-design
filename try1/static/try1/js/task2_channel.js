$(function () {
    let $form = $('form#form');
    var $answer_el;
    var $btn_answer = $('button.answer');
    socket.onmessage = function (event) {
        var obj = jQuery.parseJSON(event.data);
        $('.form_container').html(obj.form_block);
    };

    ;
    $btn_answer.on('click', function () {
        let input_type = $("[name='question']").attr('type');
        $answer_el = $("[name='question']");
        var question_body = $('label[for="id_question"]');
        jQuery.validator.addMethod("correct_answer", function (value, element) {
            let correct_answer = question_body.text();
            console.log('we are within our custom validator');
            return this.optional(element) || value === correct_answer;
        }, "Please type this answer exactly as the text provided above");
        let validator = $form.validate({
            rules: {
                question: {correct_answer: true}
            },
            errorPlacement: function (error, element) {
                if (element.attr("name") === "question") {
                    $( "<p>Please type this answer exactly as the text provided above</p>" ).insertAfter(".otree-modal-message");
                }
            }
        });
        if (validator.form() === true) {
            let answer = $answer_el.val();

            //let task_id = $answer_el.data('task');
            var msg = {
                'answer': answer,
                //'question': question
                //'task_id': task_id,
            };
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify(msg));
            }
            ;
        } else {
            $('#error_modal').modal('show');
        }
        ;
    validator.destroy()

    });
    $form.keydown(function (e) {
        if (e.keyCode == 13) {
            if (event.keyCode === 13) {
                event.preventDefault();
                $btn_answer.click();
                return false;
            }
        }
    });
    //No Copy/Paste
        var ctrlDown = false,
        ctrlKey = 17,
        cmdKey = 91,
        vKey = 86,
        cKey = 67;

    $(document).keydown(function(e) {
        if (e.keyCode == ctrlKey || e.keyCode == cmdKey) ctrlDown = true;
    }).keyup(function(e) {
        if (e.keyCode == ctrlKey || e.keyCode == cmdKey) ctrlDown = false;
    });

    $(document).keydown(function(e) {
        if (ctrlDown && (e.keyCode == vKey || e.keyCode == cKey)) return false;
    });

    // Document Ctrl + C/V
    $(document).keydown(function(e) {
        if (ctrlDown && (e.keyCode == cKey)) console.log("Document catch Ctrl+C");
        if (ctrlDown && (e.keyCode == vKey)) console.log("Document catch Ctrl+V");
    });

});