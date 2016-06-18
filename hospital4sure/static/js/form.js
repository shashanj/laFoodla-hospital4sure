    var lat = -33.8688
    var lng = 151.2195
    var map;
    $(document).ready(function() {

      var shown = true

       $('.datepicker').pickadate({
        selectMonths: true, 
        selectYears: 50 , 
      })

      registerautoclick();
      registerclclick(shown);
      registersearch();
      initAutocompleteAddress1();
      initAutocompleteAddress2();
      $('select').material_select();
    });

    function initAutocomplete(node) {

          map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: lat, lng: lng},
          zoom: 13,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        google.maps.event.addListener(map, "idle", function(){
          google.maps.event.trigger(map, 'resize'); 
        });
        if (lat !=-33.8688 && lng !=151.2195 ) {
              $(node).attr('value', lat + ',' + lng)
              $(node).attr('type', 'text')
              
              var marker = new google.maps.Marker({
                position: map.getCenter(),
                map: map,
                title: 'Your selected location!!'
            });
        }

        // Create the search box and link it to the UI element.
        var input = document.getElementById('pac-input');
        var searchBox = new google.maps.places.SearchBox(input);
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        // Bias the SearchBox results towards current map's viewport.
        map.addListener('bounds_changed', function() {
          searchBox.setBounds(map.getBounds());
        });

        var markers = [];
        // Listen for the event fired when the user selects a prediction and retrieve
        // more details for that place.
        searchBox.addListener('places_changed', function() {
          var places = searchBox.getPlaces();
          if (places.length == 0) {
            return;
          }

          // Clear out the old markers.
          markers.forEach(function(marker) {
            marker.setMap(null);
          });
          markers = [];
          // For each place, get the icon, name and location.
          var bounds = new google.maps.LatLngBounds();
          places.forEach(function(place) {
            var icon = {
              url: place.icon,
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };

            // Create a marker for each place.
            markers.push(new google.maps.Marker({
              map: map,
              icon: icon,
              title: place.name,
              position: place.geometry.location
            }));
            
            /////////////////////////////////
              lat =  place.geometry.location.lat()
              long = place.geometry.location.lng()
              
              $(node).attr('value', lat + ',' + long)
              $(node).attr('type', 'text')
              
            ///////////////////////////////////
            if (place.geometry.viewport) {
              bounds.union(place.geometry.viewport);
            } else {
              bounds.extend(place.geometry.location);
            }
          });
          map.fitBounds(bounds);
        });        
    
    }
    var par = ''
    function registeraddclick(node,id){
      if($(node).attr('value') == 0){
        par = $('#'+id).html()
        mode = $.parseHTML(par)
        $(mode).children().each(function(){
          $(this).attr('class', Number(id) +'_'+ 1 )
        })
        $('#'+id).append(mode)
        $(node).attr('value',1)
        $(node).prev().attr('value',1)
      }
      else{
          mode = $.parseHTML(par)           
          $(mode).children().each(function(){
            $(this).attr('class', Number(id)+ '_' +  (Number($(node).attr('value'))+1) )
          })
          $('#'+id).append(mode)          
          $(node).attr('value',Number($(node).attr('value'))+1)
          $(node).prev().attr('value',$(node).attr('value'))          
      }
 
    }

    function registerremoveclick(node,id){
      remove = Number(id) + '_'+ Number($(node).next().attr('value'))
      $('.'+ remove).remove()
      if(Number($(node).attr('value')) > 0){
        $(node).next().attr('value', Number($(node).next().attr('value')) - 1)
        $(node).attr('value', Number($(node).next().attr('value')))
      }
    }

    function registerautoclick(){
      $('#auto').on('click',function(){
        if($('.sec').is(':visible') === true){
          $('.sec').hide()
        }
        else{
          $('.sec').show()
        }
      })
    }

    function registerclclick(shown){
      $('.cl').on('click', function(){
        if(shown == true){
          initAutocomplete(this.getElementsByTagName("INPUT"))
          shown = false
        }        
      })
    }

    function registersearch(){
      $('#pac-input').on('keydown',function(event){
         if(event.keyCode == 13) {
            event.preventDefault();
            return false;
          }
      })
    }

    var placeSearch, autocomplete, autocomplete2;
    var componentForm = {
      street_number: 'short_name',
      route: 'long_name',
      locality: 'long_name',
      sublocality_level_1: 'long_name',
      administrative_area_level_1: 'long_name',
      postal_code: 'short_name'
    };


    function initAutocompleteAddress1() {
      // Create the autocomplete object, restricting the search to geographical
      // location types.
      autocomplete = new google.maps.places.Autocomplete(
          /** @type {!HTMLInputElement} */(document.getElementById('autocomplete')),
          {types: ['geocode']});

      // When the user selects an address from the dropdown, populate the address
      // fields in the form.
      autocomplete.addListener('place_changed', fillInAddress);
    }

    function fillInAddress() {
      // Get the place details from the autocomplete object.
      var place = autocomplete.getPlace();

      for (var component in componentForm) {
        document.getElementById(component+'-1').value = '';
        document.getElementById(component+'-1').disabled = false;
      }
      lat = place.geometry.location.lat();
      lng = place.geometry.location.lng()
      // Get each component of the address from the place details
      // and fill the corresponding field on the form.
      for (var i = 0; i < place.address_components.length; i++) {
        var addressType = place.address_components[i].types[0];
        if (componentForm[addressType]) {
          var val = place.address_components[i][componentForm[addressType]];
          document.getElementById(addressType+'-1').value = val;
        }
      }
    }

    function initAutocompleteAddress2() {
      // Create the autocomplete object, restricting the search to geographical
      // location types.
      autocomplete2 = new google.maps.places.Autocomplete(
          /** @type {!HTMLInputElement} */(document.getElementById('autocomplete2')),
          {types: ['geocode']});

      // When the user selects an address from the dropdown, populate the address
      // fields in the form.
      autocomplete2.addListener('place_changed', fillInAddress2);
    }

    function fillInAddress2() {
      // Get the place details from the autocomplete object.
      var place = autocomplete2.getPlace();

      for (var component in componentForm) {
        document.getElementById(component+'-2').value = '';
        document.getElementById(component+'-2').disabled = false;
      }

      // Get each component of the address from the place details
      // and fill the corresponding field on the form.
      for (var i = 0; i < place.address_components.length; i++) {
        var addressType = place.address_components[i].types[0];
        if (componentForm[addressType]) {
          var val = place.address_components[i][componentForm[addressType]];
          document.getElementById(addressType+'-2').value = val;
          
        }
      }
    }

    // Bias the autocomplete object to the user's geographical location,
    // as supplied by the browser's 'navigator.geolocation' object.
    function geolocate() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          var geolocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          var circle = new google.maps.Circle({
            center: geolocation,
            radius: position.coords.accuracy
          });
          autocomplete.setBounds(circle.getBounds());
          autocomplete2.setBounds(circle.getBounds());
        });
      }
    }
