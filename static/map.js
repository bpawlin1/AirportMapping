require([
    'esri/Map',
    'esri/views/MapView',
    'esri/layers/GeoJSONLayer',
    'esri/widgets/FeatureTable',
    "esri/core/reactiveUtils",
  ], function (Map, MapView, GeoJSONLayer, FeatureTable, reactiveUtils) {
    var map = new Map({
      basemap: 'topo-vector'
    });
  
    var view = new MapView({
      container: 'viewDiv',
      map: map,
      center: [-96, 37],
      zoom: 4
    });
  
    // Create a GeoJSONLayer
    var geojsonLayer = new GeoJSONLayer({
      url: '/airports/geojson',
      popupTemplate: {
        title: '{airport}',
        content: '<b>Country:</b> {country_code}<br><b>Region:</b> {region_name}<br><b>IATA:</b> {iata}<br><b>ICAO:</b> {icao}'
      }
    });
    map.add(geojsonLayer);
  
    // Create a feature table for the airports
    var featureTable = new FeatureTable({
      view: view,
      layer: geojsonLayer,
      container: 'table',
      visibleElements: { // autocast to VisibleElements
        menuItems: {
          clearSelection: true,
          refreshData: true,
          toggleColumns: true,
          selectedRecordsShowAllToggle: true,
          selectedRecordsShowSelectedToggle: true,
          zoomToSelection: true
        }
      },
    });
  
    reactiveUtils.when(
        () => view.stationary === true,
        () => {
          // Get the new extent of view/map whenever map is updated.
          if (view.extent) {
            // Filter out and show only the visible features in the feature table.
            featureTable.filterGeometry = view.extent;
          }
        }, {initial: true}
      );
      
      // Listen for the view's click event and access the associated graphic.

      view.on("immediate-click", (event) => {
        view.hitTest(event).then((response) => {
          candidate = response.results.find((result) => {
            return (
              result.graphic &&
              result.graphic.layer &&
              result.graphic.layer === geojsonLayer

            );
          });

          // Add the graphic's ObjectId into the collection of highlightIds.
          // Check that the featureTable.highlightIds collection
          // does not include an already highlighted feature.
          if (candidate) {
            const objectId = candidate.graphic.getObjectId();

            if (featureTable.highlightIds.includes(objectId)) {
              // Remove feature from current selection if feature
              // is already added to highlightIds collection
              featureTable.highlightIds.remove(objectId);
            } else {
              // Add this feature to the featureTable highlightIds collection
              featureTable.highlightIds.add(objectId);
            }
          }
        });
      });

      // Watch the featureTable's highlightIds.length property,
      // and get the count of highlighted features within
      // the table.

      featureTable.watch("highlightIds.length", (ids) => {
        highlightIdsCount = ids;

        // Iterate through the filters within the table.
        // If the active filter is "Show selection",
        // changes made to highlightIds (adding/removing)
        // are reflected.

        featureTable.viewModel.activeFilters.forEach((filter) => {
          if (filter.type === "selection") {
            selectionIdCount = filter.objectIds.length; // the filtered selection's id count
            // Check that the filter selection count is equal to the
            // highlightIds collection count. If not, update filter selection.
            if (selectionIdCount !== highlightIdsCount) {
              featureTable.filterBySelection();
            }
          }
        });
      });
    
  
});