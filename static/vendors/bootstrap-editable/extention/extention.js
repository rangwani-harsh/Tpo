/**
Address editable input.
Internally value stored as {institute: "Moscow", hostelName: "Lenina", roomNo: "15"}

@class address
@extends abstractinput
@final
@example
<a href="#" id="address" data-type="address" data-pk="1">awesome</a>
<script>
$(function(){
    $('#address').editable({
        url: '/post',
        title: 'Enter institute, hostelName and roomNo #',
        value: {
            institute: "Moscow", 
            hostelName: "Lenina", 
            roomNo: "15"
        }
    });
});
</script>
**/
(function ($) {
    "use strict";
    
    var Address = function (options) {
        this.init('address', options, Address.defaults);
    };

    //inherit from Abstract input
    $.fn.editableutils.inherit(Address, $.fn.editabletypes.abstractinput);

    $.extend(Address.prototype, {
        /**
        Renders input from tpl

        @method render() 
        **/        
        render: function() {
           this.$input = this.$tpl.find('input');
        },
        
        /**
        Default method to show value in element. Can be overwritten by display option.
        
        @method value2html(value, element) 
        **/
        value2html: function(value, element) {
            if(!value) {
                $(element).empty();
                return; 
            }
            var html = $('<div>').text(value.institute).html() + ', ' + $('<div>').text(value.hostelName).html() + ' st., bld. ' + $('<div>').text(value.roomNo).html();
            $(element).html(html); 
        },
        
        /**
        Gets value from element's html
        
        @method html2value(html) 
        **/        
        html2value: function(html) {        
          /*
            you may write parsing method to get value by element's html
            e.g. "Moscow, st. Lenina, bld. 15" => {institute: "Moscow", hostelName: "Lenina", roomNo: "15"}
            but for complex structures it's not recommended.
            Better set value directly via javascript, e.g. 
            editable({
                value: {
                    institute: "Moscow", 
                    hostelName: "Lenina", 
                    roomNo: "15"
                }
            });
          */ 
          return null;  
        },
      
       /**
        Converts value to string. 
        It is used in internal comparing (not for sending to server).
        
        @method value2str(value)  
       **/
       value2str: function(value) {
           var str = '';
           if(value) {
               for(var k in value) {
                   str = str + k + ':' + value[k] + ';';  
               }
           }
           return str;
       }, 
       
       /*
        Converts string to value. Used for reading value from 'data-value' attribute.
        
        @method str2value(str)  
       */
       str2value: function(str) {
           /*
           this is mainly for parsing value defined in data-value attribute. 
           If you will always set value by javascript, no need to overwrite it
           */
           return str;
       },                
       
       /**
        Sets value of input.
        
        @method value2input(value) 
        @param {mixed} value
       **/         
       value2input: function(value) {
           if(!value) {
             return;
           }
           this.$input.filter('[name="institute"]').val(value.institute);
           this.$input.filter('[name="hostelName"]').val(value.hostelName);
           this.$input.filter('[name="roomNo"]').val(value.roomNo);
       },       
       
       /**
        Returns value of input.
        
        @method input2value() 
       **/          
       input2value: function() { 
           return {
              institute: this.$input.filter('[name="institute"]').val(), 
              hostelName: this.$input.filter('[name="hostelName"]').val(), 
              roomNo: this.$input.filter('[name="roomNo"]').val()
           };
       },        
       
        /**
        Activates input: sets focus on the first field.
        
        @method activate() 
       **/        
       activate: function() {
            this.$input.filter('[name="institute"]').focus();
       },  
       
       /**
        Attaches handler to submit form in case of 'showbuttons=false' mode
        
        @method autosubmit() 
       **/       
       autosubmit: function() {
           this.$input.keydown(function (e) {
                if (e.which === 13) {
                    $(this).closest('form').submit();
                }
           });
       }       
    });

    Address.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
        tpl: '<div class="editable-address"><label><span>Institute: </span><input type="text" name="institute" class="input-small"></label></div>'+
             '<div class="editable-address"><label><span>Hostel Name: </span><input type="text" name="hostelName" class="input-small"></label></div>'+
             '<div class="editable-address"><label><span>Room No: </span><input type="text" name="roomNo" class="input-mini"></label></div>',
             
        inputclass: ''
    });

    $.fn.editabletypes.address = Address;

}(window.jQuery));