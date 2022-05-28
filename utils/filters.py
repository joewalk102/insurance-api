from rest_framework import filters


class AllowStaffLimitUserFilterBackend(filters.BaseFilterBackend):
    """
    Filter out records that do not apply to the user if the
    user is not a staff member. If they are staff, they can
    see all other results.
    """

    def filter_queryset(self, request, queryset, view):
        if request.user.is_staff:
            return queryset
        return queryset.filter(user=request.user)
