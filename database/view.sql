create definer = admin@localhost view view_promotion as
select `p`.`id_promotion`     AS `id_promotion`,
       `p`.`promotion_name`   AS `promotion_name`,
       `p`.`p_start_date`     AS `p_start_date`,
       `p`.`p_end_date`       AS `p_end_date`,
       `p`.`percent_discount` AS `percent_discount`,
       `r`.`name_type`        AS `name_type`
from ((`dormitory`.`promotion` `p` join `dormitory`.`apply_promotion` `a`
       on ((`p`.`id_promotion` = `a`.`id_promotion`))) join `dormitory`.`room_type` `r`
      on ((`a`.`id_type` = `r`.`id_type`)));

create definer = admin@localhost view view_room_not_cleaned as
select `l`.`room_number` AS `room_number`
from ((select `dormitory`.`reservation`.`room_number`         AS `room_number`,
              max(`dormitory`.`reservation`.`check_out_date`) AS `max(check_out_date)`
       from `dormitory`.`reservation`
       where (now() >= `dormitory`.`reservation`.`check_out_date`)
       group by `dormitory`.`reservation`.`room_number`) `l` left join (select `dormitory`.`cleaning`.`room_number`        AS `room_number`,
                                                                               max(`dormitory`.`cleaning`.`cleaning_date`) AS `max(cleaning_date)`
                                                                        from `dormitory`.`cleaning`
                                                                        group by `dormitory`.`cleaning`.`room_number`) `p`
      on ((`p`.`room_number` = `l`.`room_number`)))
where (`p`.`room_number` is null);
