function init_map(members) {
	// Show the loading indicator first
	var map_options = { 
    'units' : "m",
    'maxResolution' : 156543.0339,
    'numZoomLevels' : 22,
    'projection' : new OpenLayers.Projection("EPSG:900913"),
    'displayProjection' : new OpenLayers.Projection("EPSG:4326"),
    'maxExtent' : new OpenLayers.Bounds(-20037508,-20037508,20037508,20037508)
	};
	    
	var data = {
              "type": "FeatureCollection", 
              "features": members
	};
  	var map = new OpenLayers.Map('map', map_options);
	
	map.layers.base = new OpenLayers.Layer.OSM.Mapnik("OpenStreetMap (Mapnik)");
	map.addLayer(map.layers.base);
  	map.addControl(new OpenLayers.Control.LayerSwitcher());
  	var toGoog = function (lonlat){
  		return lonlat.transform(new OpenLayers.Projection("EPSG:4326"),
			new OpenLayers.Projection("EPSG:900913"));
  	}
	var gj = new OpenLayers.Format.GeoJSON();
   	var vector = new OpenLayers.Layer.Vector(); 
   	map.addLayer(vector);
   	vector.addFeatures(gj.read(data));
  	var center = toGoog(new OpenLayers.LonLat(-122.29, 47.65));
	map.setCenter(center,6);
	map.updateSize();

	//Hide the loading div
	jQuery("#loading").hide();
}
	    