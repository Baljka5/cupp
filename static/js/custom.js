/* ------------------------------------------------------------------------------
 *
 *  # Custom JS code
 *
 *  Place here all your custom js. Make sure it's loaded after app.js
 *
 * ---------------------------------------------------------------------------- */

var js = {};
var map;
var markers = [];
var circles = [];

function handleMarker(marker, pointId) {
  marker.addListener('click', function () {
    $.ajax({
      url: `/info/${pointId}/`,
      dataType: 'html',
      success: function (data) {
        if (js.mapInfoWindow) {
          js.mapInfoWindow.close();
        }

        js.mapInfoWindow = new google.maps.InfoWindow({
          content: data
        });

        google.maps.event.addListener(js.mapInfoWindow, 'domready', function () {

          var iwOuter = $('.gm-style-iw');
          iwOuter.next().hide();

          $('.gm-style-iw [data-toggle=tooltip]').tooltip({
            container: 'body'
          });

          $('[data-popup="lightbox"]').fancybox({
            padding: 3
          });
        });

        js.mapInfoWindow.open(map, marker);
      }
    });
  });
}

function addMarker() {
  $('#id_map_data ul').each(function (inx, obj) {
    var latitude = parseFloat($(obj).data('lat'));
    var longitude = parseFloat($(obj).data('lon'));
    var pointId = $(obj).data('id');
    var type = $(obj).data('type');
    var radius = $(obj).data('radius');
    var latLng = {lat: latitude, lng: longitude};
    var marker = new google.maps.Marker({
      position: latLng,
      map: map,
      title: $(obj).data('title'),
      icon: {
        url: `/static/images/ui/marker-${type}.png`,
        size: new google.maps.Size(38, 54),
        scaledSize: new google.maps.Size(19, 27),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(10, 27)
      }
    });
    marker.type = type;
    marker.circle = addCircle(map, marker, radius);
    markers.push(marker);
    handleMarker(marker, pointId);
  });
}

function addCircle(map, marker, radius) {
  if (!radius) return;

  var circle = new google.maps.Circle({
    map: map,
    radius: parseInt(radius),    // 10 miles in metres
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 0.35,
    fillColor: '#FF0000',
    fillOpacity: 0.35,
  });

  circle.bindTo('center', marker, 'position');
  return circle;
}

function setMarker(map) {
  for (var i = 0; i < markers.length; i++) {
    var _marker = markers[i];

    _marker.setMap(map);
    if (_marker.circle) {
      if ($('#id_radius').is(':checked'))
        _marker.circle.setMap(map)
      else
        _marker.circle.setMap(null)
    }
  }
}

function clearMarker() {
  for (var i = 0; i < markers.length; i++) {
    var _marker = markers[i];
    if (_marker.circle) {
      _marker.circle.setMap(null)
    }

    _marker.setMap(null)
  }
  markers = []
}

function maploadList(map, changed) {
  if (changed) {
    localStorage.removeItem('formFilter');
  }

  //var cachedData = localStorage.getItem('formFilter');
  //var filterQuery = cachedData || $('#form_filter').serialize();
  var filterQuery = $('#form_filter').serialize();

  $.ajax({
    url: '/ajax-points/',
    data: filterQuery,
    dataType: 'html',
    success: function (response) {
      localStorage.setItem('formFilter', filterQuery)
      clearMarker();
      $('#id_map_data').html(response)
      addMarker();
      setMarker(map);
    }
  })
}

function initMap() {

  var mapOptions = {
    center: {lat: 47.9156, lng: 106.9130},
    scrollwheel: false,
    zoom: 13,
    mapTypeControl: true,
    fullscreenControl: false,
    mapTypeControlOptions: {
      mapTypeIds: ['roadmap', 'satellite'],
      position: google.maps.ControlPosition.TOP_RIGHT
    },
    controlSize: 24,
    styles: [
      {
        "featureType": "administrative.country",
        "elementType": "geometry",
        "stylers": [
          {
            "visibility": "simplified"
          },
          {
            "hue": "#ff0000"
          }
        ]
      }
    ]
  };

  map = new google.maps.Map(document.getElementById('map'), mapOptions);

  maploadList(map);
}

// String prototypes
String.prototype.trim = function () {
  return this.replace(/^\s+|\s+$/g, '');
};
String.prototype.startsWith = function (prefix) {
  return this.indexOf(prefix) === 0;
};
String.prototype.endsWith = function (suffix) {
  return this.indexOf(suffix, this.length - suffix.length) !== -1;
};
String.prototype.format = String.prototype.f = function () {
  var args = arguments;
  return this.replace(/\{\{|\}\}|\{(\d+)\}/g, function (m, n) {
    if (m === '{{') {
      return '{';
    }
    if (m === '}}') {
      return '}';
    }
    return args[n];
  });
};

$(function () {
  var menus = $('.navbar a[href="{0}"], .navbar-nav .dropdown-menu a[href="{0}"]'.f(window.location.pathname));

  menus.each(function (index) {
    $(this).parent().addClass('active');
    if ($(this).parent().parent().hasClass('dropdown-menu')) {
      $(this).parent().parent().parent().addClass('active');
      $(this).parent().removeClass('active');
    }
  });

  var inactivityTime = function () {
    var time;
    window.onload = resetTimer;
    // DOM Events
    document.onmousemove = resetTimer;
    document.onkeypress = resetTimer;

    function logout() {
        location.href = '/logout/'
    }

    function resetTimer() {
        clearTimeout(time);
        time = setTimeout(logout, 1000 * 60 * 5)
        // 1000 milliseconds = 1 second
    }
  };

  inactivityTime()
});