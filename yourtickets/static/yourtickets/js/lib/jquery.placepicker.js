/*! jquery-placepicker 19-09-2016 */
+function(a,b){function c(c,d){function e(){var a='<div class="input-group"><span class="input-group-btn"><button type="button" data-toggle="collapse" href="#'+d.mapContainerId+'" class="btn btn-default"><span class="'+d.mapIconClass+'"></span></button></span></div>';return a}function f(){if(d.mapContainerId){var b=a(c),f=b.parent(),g=f.children().index(c);b.replaceWith(e()),f.children().eq(g).append(c)}}function g(a){if(a){var b={query:a};w&&w.textSearch(b,function(a,b){if(b===google.maps.places.PlacesServiceStatus.OK)for(var c=0;c<a.length;c++)return void o(a[c])})}}function h(a){v.geocode({latLng:a},function(a,b){if(b===google.maps.GeocoderStatus.OK&&a[0]){var c=a[0];o(c,!1)}})}function i(){return q=a(d.map).get(0),q||d.mapContainerId&&(q=a("#"+d.mapContainerId+" .placepicker-map").get(0)),!!q}function j(){i()&&(r=new google.maps.Map(q,d.mapOptions),t.bindTo("bounds",r),google.maps.event.addListener(r,"click",function(a){var b=a.latLng;s.setPosition(b),r.panTo(b),c.blur(),h(b)}),s=new google.maps.Marker({map:r}),w=new google.maps.places.PlacesService(r),a(q).parent().on("show.bs.collapse",function(b){a(b.target).css("display","block").find("img[src*='gstatic.com/'], img[src*='googleapis.com/']").css("max-width","none"),c.value?u.resize():u.geoLocation(),a(b.target).css("display","")}))}function k(){t=new google.maps.places.Autocomplete(c,d.autoCompleteOptions),google.maps.event.addListener(t,"place_changed",function(){var a=t.getPlace();a.geometry&&o(a)})}function l(){u.resize.call(u)}function m(){function b(b,e){if("keydown"===b){var f=e;e=function(b){var d=a(".pac-item-selected").length>0;if((13===b.which||13===b.keyCode)&&!d){var e=a.Event("keydown",{keyCode:40,which:40});f.apply(c,[e])}f.apply(c,[b])}}d.apply(c,[b,e])}var d=c.addEventListener?c.addEventListener:c.attachEvent;c.addEventListener=b,c.attachEvent=b}function n(){if(v=new google.maps.Geocoder,m(),f(),k(),j(),c.value)g(c.value);else{var e=d.latitude||a(d.latitudeInput).prop("value"),h=d.longitude||a(d.longitudeInput).prop("value");e&&h&&u.setLocation(e,h)}a(b).on("resize",l),a(c).on("keypress",function(a){d.preventSubmit&&13===a.keyCode&&(a.preventDefault(),a.stopImmediatePropagation())})}function o(b,e){e="undefined"==typeof e,x=b,u.resize();var f=b.geometry.location;e&&p(f),a(d.latitudeInput).prop("value",f.lat()),a(d.longitudeInput).prop("value",f.lng()),e||(c.value=b.formatted_address),"function"==typeof d.placeChanged&&d.placeChanged.call(u,b)}function p(a){if(r){r.setCenter(a);var b=d.icon||d.placesIcon&&place.icon?place.icon:null;if(b){var c={url:b,size:new google.maps.Size(71,71),origin:new google.maps.Point(0,0),anchor:new google.maps.Point(17,34),scaledSize:new google.maps.Size(35,35)};s.setIcon(c)}s.setPosition(a),s.setVisible(!0)}}var q,r,s,t,u=this,v=null,w=null,x=null,y=null;this.setValue=function(a){c.value=a,g(a)},this.getValue=function(){return c.value},this.setLocation=function(a,b){var c=new google.maps.LatLng(a,b);this.setLatLng(c)},this.getLocation=function(){var a=this.getLatLng();return{latitude:a&&a.lat()||d.latitude,longitude:a&&a.lng()||d.longitude}},this.setLatLng=function(a){y=a,h(y)},this.getLatLng=function(){return x&&x.geometry?x.geometry.location:y},this.getMap=function(){return r},this.reload=function(){r&&g(c.value)},this.resize=function(){if(r){var a=r.getCenter();google.maps.event.trigger(r,"resize"),r.setCenter(a)}},this.geoLocation=function(a){navigator.geolocation?navigator.geolocation.getCurrentPosition(function(b){var c=new google.maps.LatLng(b.coords.latitude,b.coords.longitude);p(c),h(c),a&&a(c)},function(){a&&a(null)}):a&&a(null)},n.call(this)}var d="placepicker",e={map:"",mapIconClass:"glyphicon glyphicon-globe",mapOptions:{zoom:15},places:{icons:!1},autoCompleteOptions:{},placeChanged:null,location:null,preventSubmit:!0},f=c;a.fn[d]=function(b){return this.each(function(){return a(this).data(d)||a(this).data(d,new f(this,a.extend({},e,b,a(this).data()))),a(this)})}}(jQuery,window);