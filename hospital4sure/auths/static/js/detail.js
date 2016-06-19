    $(document).ready(function() {
      var shown = true

       $('.datepicker').pickadate({
        selectMonths: true, 
        selectYears: 50 , 
      })

      registerautoclick();
      registerclclick(shown);
      registersearch();
      $('select').material_select();
    });

    function initAutocomplete(node) {
        ans= $('#mapvalue').attr('value').split(',')
        lat = Number(ans[0])
        lng = Number(ans[1])
        myLatLng = {'lat': lat, 'lng': lng}
        var map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: lat, lng: lng},
          zoom: 13,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });
        var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          title: 'Your selected location!!'
        });
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
      console.log($(node).next().attr('value'))
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