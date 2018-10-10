(function ($) {
    "use strict";

    /*==================================================================
    [ Validate after type ]*/
    $('.validate-input .input100').each(function () {
        $(this).on('blur', function () {
            if (validate(this) == false) {
                showValidate(this);
            } else {
                $(this).parent().addClass('true-validate');
            }
        })
    })


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('#update').click(function (e) {
        var check = true;

        for (var i = 0; i < input.length; i++) {
            if (validate(input[i]) == false) {
                showValidate(input[i]);
                check = false;
            }
        }

        if (check) {
            e.preventDefault();
            var patient_id = $("#patient-send").val()
            var next_stage = $("#next-stage").val()
            var advice = $("#advice").val()
            console.log(patient_id)
            $.ajax({
                type: "POST",
                url: 'https://am39ynfw8i.execute-api.us-east-1.amazonaws.com/karina-v1',
                //dataType: 'json',
                crossDomain: true,
                contentType: 'application/json',
                data: JSON.stringify({
                    'patientid': patient_id,
                    'nextstage': next_stage,
                    'advice': advice

                }),
                success: function (res) {
                    //console.log("Success")
                    if(JSON.stringify(res) == JSON.stringify("Success")){
                        $('#form-response2').html('<div class="alert alert-success" role="alert">Success!</div>');
                    } else {
                        $('#form-response2').html('<div class="alert alert-danger" role="alert">Unsuccessful. Please check if the patient is in the records.</div>');
                    }
                    //console.log(res);
                },
                error: function () {
                    $('#form-response2').html(
                        '<div class="alert alert-info" role="alert">Something went wrong... We are working on it!</div>');
                }
            });
        }

        return check;
    });


    $('.validate-form .input100').each(function () {
        $(this).focus(function () {
            hideValidate(this);
            $(this).parent().removeClass('true-validate');
        });
    });

    function validate(input) {
        if ($(input).attr('name') == 'patient-id') {
            if ($(input).val().trim().match(/^[p][0-9]{3}$/) == null) {
                return false;
            }
        } else {
            if ($(input).val().trim() == '') {
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');

        $(thisAlert).append('<span class="btn-hide-validate">&#xf136;</span>')
        $('.btn-hide-validate').each(function () {
            $(this).on('click', function () {
                hideValidate(this);
            });
        });
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate');
        $(thisAlert).find('.btn-hide-validate').remove();
    }


})(jQuery);



(function ($) {
    "use strict";

    /*==================================================================
    [ Validate after type ]*/
    $('.validate-input1 .input100').each(function () {
        $(this).on('blur', function () {
            if (validate(this) == false) {
                showValidate(this);
            } else {
                $(this).parent().addClass('true-validate');
            }
        })
    })


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input1 .input100');

    $("#retrieve").click(function (e) {
        var check = true;

        for (var i = 0; i < input.length; i++) {
            if (validate(input[i]) == false) {
                showValidate(input[i]);
                check = false;
            }
        }

        if (check) {
            e.preventDefault();
            var patient_id = $('#patient-ret').val();
            $.ajax({
                type: "GET",
                url: 'https://am39ynfw8i.execute-api.us-east-1.amazonaws.com/karina-v1',
                //dataType: 'json',
                crossDomain: true,
                contentType: 'application/x-www-form-urlencoded',
                data: "patientid=" + patient_id,
                success: function (res) {

                    var html_str = '<table id="t01"><tr><th>Doctor</th><th>Last Appointment</th><th>Next Appointment</th><th>Last Stage</th><th>Current Stage</th><th>Advice</th></tr>'
                    var arr = JSON.parse(JSON.stringify(res))
                    console.log(arr)
                    for (i = 0; i < arr.length; i++) {                        
                        var row = "<tr>"
                        row = row + "<td>" + arr[i].doctor + "</td>"
                        row = row + "<td>" + arr[i].prev_appt + "</td>"
                        row = row + "<td>" + arr[i].next_appt + "</td>"
                        row = row + "<td>" + arr[i].prev_stage + "</td>"
                        row = row + "<td>" + arr[i].next_stage + "</td>"
                        row = row + "<td>" + arr[i].advice + "</td>"
                        
                        row += "</tr>"
                        html_str += row
                    }
                    html_str += "</table"
                    $('#form-response').html(html_str);
                },
                error: function () {
                    $('#form-response').html(
                        '<div class="alert alert-info" role="alert">Something went wrong... We are working on it!</div>');
                }
            });
        }

        return check;
    });


    $('.validate-form1 .input100').each(function () {
        $(this).focus(function () {
            hideValidate(this);
            $(this).parent().removeClass('true-validate');
        });
    });

    function validate(input) {
        if ($(input).attr('name') == 'patient-id') {
            if ($(input).val().trim().match(/^[p][0-9]{3}$/) == null) {
                return false;
            }
        } else {
            if ($(input).val().trim() == '') {
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');

        $(thisAlert).append('<span class="btn-hide-validate">&#xf136;</span>')
        $('.btn-hide-validate').each(function () {
            $(this).on('click', function () {
                hideValidate(this);
            });
        });
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate');
        $(thisAlert).find('.btn-hide-validate').remove();
    }


})(jQuery);