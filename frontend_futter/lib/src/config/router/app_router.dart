import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/presentation/views/intro_view.dart';

part 'app_router.gr.dart';

@AutoRouterConfig(replaceInRouteName: 'View,Route')
class AppRouter extends _$AppRouter {
  @override
  List<AutoRoute> get routes => [
        AutoRoute(page: IntroRoute.page, initial: true),
      ];
}
