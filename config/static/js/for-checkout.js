(function () {
    var $container = $(document.getElementById('address_zip'));


    var $zip = $container.find('[name="zip"]'),
        $region = $container.find('[name="region"]'),
        $district = $container.find('[name="district"]'),
        $city = $container.find('[name="city"]'),
        $street = $container.find('[name="street"]'),
        $building = $container.find('[name="building"]');
    $()
        .add($region)
        .add($district)
        .add($city)
        .add($street)
        .add($building)
        .fias({
            parentInput: $container.find('.js-form-address'),
            verify: false,
        });

    $region.fias('type', $.fias.type.region);
    $district.fias('type', $.fias.type.district);
    $city.fias('type', $.fias.type.city);
    $street.fias('type', $.fias.type.street);
    $building.fias('type', $.fias.type.building);

    $district.fias('withParents', true);
    $city.fias('withParents', true);
    $street.fias('withParents', true);


    // Подключаем плагин для почтового индекса
    $zip.fiasZip($container, function(obj){
        $region.removeAttr('disabled');
        $district.removeAttr('disabled');
        $city.removeAttr('disabled');
        $street.removeAttr('disabled');
        $building.removeAttr('disabled');
    });

})();