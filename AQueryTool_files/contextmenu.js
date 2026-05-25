angular.module('ui.bootstrap.contextMenu', [])

.directive('contextMenu', ["$parse", "$q", function ($parse, $q) {

    var contextMenus = [];

    var removeContextMenus = function (level) {
        while (contextMenus.length && (!level || contextMenus.length > level)) {
            contextMenus.pop().remove();
        }
        if (contextMenus.length == 0 && $currentContextMenu) {
            $currentContextMenu.remove();
        }
    };

    var $currentContextMenu = null;

    var renderContextMenu = function ($scope, event, options, model, level) {

        // 마우스 클릭해서 팝업이 뜬거라면 
        //    - 기존에 뜬 팝업 모두 닫기.
        //    - 위치 이벤트 보내기.
        if (event.button != undefined) {
            removeContextMenus(0);
            $scope.$broadcast('onContextMenu', { ctLeft: event.pageX, ctTop: event.pageY });
        }

        if (!level) { level = 0; }
        if (!$) { var $ = angular.element; }
        $(event.currentTarget).addClass('context');
        var $contextMenu = $("<div>");
        if ($currentContextMenu) {
            $contextMenu = $currentContextMenu;
        } else {
            $currentContextMenu = $contextMenu;
        }
        $contextMenu.addClass('dropdown clearfix');

        var $ul = $('<ul>');

        // 컨텍스트 메뉴를 직접 닫기 위해서 아이디 설정
        $ul.attr("id", "mouse-r-context-menu");

        $ul.addClass('dropdown-menu');
        $ul.attr({ 'role': 'menu' });
        $ul.css({
            display: 'block',
            position: 'absolute',
            left: event.pageX + 'px',
            top: event.pageY + 'px',
            "z-index": 10000
        });
        angular.forEach(options, function (item, i) {
            var $li = $('<li>');
            if (item === null) {
                $li.addClass('divider');
            } else {
                var nestedMenu = angular.isArray(item[1])
                  ? item[1] : angular.isArray(item[2])
                  ? item[2] : angular.isArray(item[3])
                  ? item[3] : null;
                var $a = $('<a>');
                $a.css("padding-right", "8px");
                $a.attr({ tabindex: '-1', href: '#' });
                var text = typeof item[0] == 'string' ? item[0] : item[0].call($scope, $scope, event, model);

                // ChatGPT가 수정한 아이콘이 들어가는 메뉴
                $q.when(text).then(function (text) {
                    var iconHtml = '';

                    if (item[3]) {
                        // item[3]이 '<'로 시작하면 HTML로 간주
                        if (typeof item[3] === 'string' && item[3].trim().startsWith('<')) {
                            iconHtml = item[3];
                        } else {
                            iconHtml = '<i class="' + item[3] + '" style="margin-right:5px;"></i>';
                        }
                    }

                    $a.html(iconHtml + text);

                    if (nestedMenu) {
                        $a.css("cursor", "default");
                        $a.append($('<strong style="font-family:monospace;font-weight:bold;float:right;">&gt;</strong>'));
                    }
                });

                //$q.when(text).then(function (text) {
                //    // 메뉴명 왼쪽에 아이콘 추가
                //    var iconHtml = item[3] ? '<i class="' + item[3] + '" style="margin-right:5px;"></i>' : '';
                //    $a.html(iconHtml + text);

                //    if (nestedMenu) {
                //        $a.css("cursor", "default");
                //        $a.append($('<strong style="font-family:monospace;font-weight:bold;float:right;">&gt;</strong>'));
                //    }
                //});

                // 원본
                //$q.when(text).then(function (text) {
                //    $a.text(text);
                //    if (nestedMenu) {
                //        $a.css("cursor", "default");
                //        $a.append($('<strong style="font-family:monospace;font-weight:bold;float:right;">&gt;</strong>'));
                //    }
                //});
                $li.append($a);

                var enabled = angular.isFunction(item[2]) ? item[2].call($scope, $scope, event, model, text) : true;
                if (enabled) {
                    var openNestedMenu = function ($event) {
                        removeContextMenus(level + 1);
                        var ev = {
                            pageX: event.pageX + $ul[0].offsetWidth - 1,
                            pageY: $ul[0].offsetTop + $li[0].offsetTop - 3
                        };
                        renderContextMenu($scope, ev, nestedMenu, model, level + 1);
                    }
                    $li.on('click', function ($event) {
                        $event.preventDefault();
                        $scope.$apply(function () {
                            if (nestedMenu) {
                                openNestedMenu($event);
                            } else {
                                $(event.currentTarget).removeClass('context');
                                removeContextMenus();
                                item[1].call($scope, $scope, event, model, text);
                            }
                        });
                    });

                    $li.on('mouseover', function ($event) {
                        $scope.$apply(function () {
                            if (nestedMenu) {
                                openNestedMenu($event);
                            }
                        });
                    });
                } else {
                    $li.on('click', function ($event) {
                        $event.preventDefault();
                    });
                    $li.addClass('disabled');
                }
            }
            $ul.append($li);
        });
        $contextMenu.append($ul);
        var height = Math.max(
            document.body.scrollHeight, document.documentElement.scrollHeight,
            document.body.offsetHeight, document.documentElement.offsetHeight,
            document.body.clientHeight, document.documentElement.clientHeight
        );

        var width = Math.max(
                document.body.scrollWidth, document.documentElement.scrollWidth,
                document.body.offsetWidth, document.documentElement.offsetWidth,
                document.body.clientWidth, document.documentElement.clientWidth
            );

        //var width = $("#rootdiv").attr("width");
        //var height = $("#rootdiv").attr("height");

        $contextMenu.css({
            width: width + 'px',
            height: height + 'px',
            position: 'absolute',
            top: 0,
            left: 0,
            zIndex: 9999
        });
        $(document).find('body').append($contextMenu);
        $contextMenu.on("mousedown", function (e) {
            if ($(e.target).hasClass('dropdown')) {
                $(event.currentTarget).removeClass('context');
                removeContextMenus();
            }
        }).on('contextmenu', function (event) {
            $(event.currentTarget).removeClass('context');
            event.preventDefault();
            removeContextMenus(level);
        });
        $scope.$on("$destroy", function () {
            removeContextMenus();
        });

        contextMenus.push($ul);
    };
    return function ($scope, element, attrs) {
        element.on('contextmenu', function (event) {
            event.stopPropagation();
            $scope.$apply(function () {
                event.preventDefault();
                var options = $scope.$eval(attrs.contextMenu);
                var model = $scope.$eval(attrs.model);
                if (options instanceof Array) {
                    if (options.length === 0) { return; }
                    renderContextMenu($scope, event, options, model);
                } else {
                    throw '"' + attrs.contextMenu + '" not an array';
                }
            });
        });
    };
}]);
