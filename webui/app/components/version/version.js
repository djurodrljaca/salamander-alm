'use strict';

angular.module('webuiApp.version', [
  'webuiApp.version.interpolate-filter',
  'webuiApp.version.version-directive'
])

.value('version', '0.1');
