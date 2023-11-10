import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/presentation/cubits/remote/versions_cubit.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class AuthGuard extends AutoRouteGuard {
  @override
  void onNavigation(NavigationResolver resolver, StackRouter router) {
    resolver.next(true);

    final context = router.navigatorKey.currentContext;
    if (context == null) return;

    final versionCubit = BlocProvider.of<VersionsCubit>(context);
    versionCubit.getVersions();
  }
}
