'use strict';

describe('webuiApp.version module', function() {
  beforeEach(module('webuiApp.version'));

  describe('version service', function() {
    it('should return current version', inject(function(version) {
      expect(version).toEqual('0.1');
    }));
  });
});
